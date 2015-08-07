from django.db import models
from django.contrib.auth.models import User
from utils.utils import relevance
from .config import MIN_RELEVANCE

# Create your models here.
class Note(models.Model):
    ''' Basic note model for holding summaries and thoughts for users, as well as linking to DataPoints'''

    title               = models.CharField(max_length=100)
    summary             = models.TextField(max_length=255)
    creation_date_time  = models.DateTimeField(auto_now_add=True)
    last_edit_date_time = models.DateTimeField(auto_now=True)
    private             = models.BooleanField()
    
    owner               = models.ForeignKey(User, null=True)
    reviewers           = models.ManyToManyField(User, related_name='note_reviewers')

    similar_notes       = models.ManyToManyField('self', related_name='similar_notes')

    last_analyzed       = models.DateTimeField(auto_now_add=True) # Used by analytics models 

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, title, summary, owner, private=True):
        return cls(title=title, summary=summary, private=private, owner=owner)

    def add_tag(self, tag):
        self.tags.add(tag)

    def add_similar_notes(self):
        '''Marks other notes as similar if they have similar tags, based on the relevance score. 
           DISREGARDS IF THE USER IS ALLOWED TO SEE THE NOTE, ALL NOTES MUST BE CHECKED BEFORE DISPLAYING 
           WHENEVER PRIVACY FEATURES ARE ADDED.'''

        # This is a super expensive operation (N^3), so we need to be careful with this
        tags = self.tag_set.all()
        for tag in tags:
            for note in tag.notes.exclude(id=self.id): # be careful no to add this note to itself
                if not self.similar_notes.filter(id=note.id).exists() and relevance(tags, note.tag_set.all()) >= MIN_RELEVANCE:                    
                    self.similar_notes.add(note)
                    for chained_note in note.similar_notes.exclude(id=self.id): # be careful to not add this note to itself
                        if not self.similar_notes.filter(id=chained_note.id).exists():                            
                            self.similar_notes.add(chained_note)
            
        
        
            
    class Meta:
        ordering = ('last_edit_date_time', 'creation_date_time', )


class DataPoint(models.Model):
    ''' Holds small bits of data that build up the details of a note'''
    datum               = models.CharField(max_length=140)
    creation_date_time  = models.DateTimeField(auto_now_add=True)
    last_edit_date_time = models.DateTimeField(auto_now=True)
    # Not sure if this is useful yet, but adding it anyway
    is_factual          = models.BooleanField()
    private             = models.BooleanField()

    owner               = models.ForeignKey(User, null=True)
    reviewers           = models.ManyToManyField(User, related_name='data_point_reviewers')    
    
    notes               = models.ManyToManyField(Note, related_name='data_points', related_query_name='data_point')

    similar_data_points = models.ManyToManyField('self', related_name='similar_data_points')

    last_analyzed       = models.DateTimeField(auto_now_add=True) # Used by analytics models 

    def __str__(self):
        return self.datum

    @classmethod
    def create(cls, datum, owner, is_factual, private, note):
        data_point = cls(datum=datum, is_factual=is_factual, private=private, owner=owner)
        data_point.notes_set.add(note)
        return data_point

    def add_tag(self, tag):
        self.tags.add(tag)

    def add_similar_data_points(self):
        ''' Adds related data points based upon tags (no NLP performed yet). Does NOT check if user has access to the data_point '''
        tags = self.tag_set.all()
        for tag in tags:
            for data_point in tag.data_points.exclude(id=self.id):
                if not self.similar_data_points.filter(id=data_point.id).exists() and relevance(tags, data_point.tag_set.all()):
                    self.similar_data_points.add(data_point)
                    for chained_point in data_point.similar_data_points.exclude(id=self.id):
                        if not self.similar_data_points.filter(id=data_point.id).exists() and relevance(tags, chained_point.tag_set.all()):
                            self.similar_data_points.add(chained_point)
    
    class Meta:
        ordering = ('last_edit_date_time', 'creation_date_time', )


class SearchQuery(models.Model):
    ''' 
    Literally just a model to hold previous search queries. PRETTY SWEET.
    Each Note can have many SearchQuery's, and each SearchQuery is treated
    as immutable with only one Note. Basically, users can have their own queries stored for them.
    '''
    query = models.CharField(max_length=255)
    date_time_queried = models.DateTimeField(auto_now_add=True) 

    note              = models.ForeignKey(Note) 
    
    # owner             = models.ForeignKey(User, null=True) # this seems like an unncessary field

    @classmethod
    def create(cls, query, note):
        query = cls(query=query, note=note)
        return query
    
    class Meta:
        ordering = ('date_time_queried', )


class Source(models.Model):
    ''' Sources for DataPoints. Notes can access these sources through their related DataPoints'''
    url            = models.CharField(max_length=255)
    found_date     = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    title          = models.CharField(max_length=30)
    data_point     = models.OneToOneField(DataPoint)
    

    def __str__(self):
        return self.url

    @classmethod
    def create(cls, url, title):
        source = cls(url=url, title=title)
        return source

    def add_tag(self, tag):
        self.tag_set.add(tag)

        

class Tag(models.Model):
    ''' Tagging for Notes, DataPoints and Sources '''
    tag           = models.CharField(max_length=16)
    creation_date = models.DateTimeField(auto_now_add=True)

    notes         = models.ManyToManyField(Note)
    data_points   = models.ManyToManyField(DataPoint)
    sources       = models.ManyToManyField(Source)
    
    def __str__(self):
        return self.tag

    @classmethod
    def create(cls, tag):
        return cls(tag=tag)

    
    
