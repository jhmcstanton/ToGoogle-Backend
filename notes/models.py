from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    ''' Basic note model for holding summaries and thoughts for users, as well as linking to DataPoints'''

    title               = models.CharField(max_length=30)
    summary             = models.TextField(max_length=255)
    creation_date_time  = models.DateTimeField(auto_now_add=True)
    last_edit_date_time = models.DateTimeField(auto_now=True)
    private             = models.BooleanField()
    
    owner               = models.ForeignKey(User)
    reviewers           = models.ManyToManyField(User)   

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, title, summary, owner, private=True):
        return cls(title=title, summmary=summary, private=private, owner=user)

    def add_tag(self, tag):
        self.tags.add(tag)
            
    class Meta:
        ordering = ('last_edit_date_time', 'creation_date_time', )


class DataPoint(models.Model):
    ''' Holds small bits of data that build up the details of a note'''
    datum               = models.CharField(max_length=50)
    creation_date_time  = models.DateTimeField(auto_now_add=True)
    last_edit_date_time = models.DateTimeField(auto_now=True)
    # Not sure if this is useful yet, but adding it anyway
    is_factual          = models.BooleanField()
    private             = models.BooleanField()

    owner               = models.ForeignKey('users.User')
    reviewers           = models.ManyToManyField('users.User')
    
    notes               = models.ManyToManyField(Note, related_name='data_points', related_query_name='data_point')

    def __str__(self):
        return self.datum

    @classmethod
    def create(cls, datum, owner, is_factual, private, note):
        data_point = cls(datum=datum, is_factual=is_factual, private=private, owner=owner)
        data_point.notes_set.add(note)
        return data_point

    def add_tag(self, tag):
        self.tags.add(tag)
    
    class Meta:
        ordering = ('last_edit_date_time', 'creation_date_time', )


class SearchQuery(models.Model):
    ''' 
    Literally just a model to hold previous search queries. PRETTY SWEET.
    Each Note can have many SearchQuery's, and each SearchQuery is treated
    as immutable with only one Note.
    '''
    query = models.CharField(max_length=255)
    date_time_queried = models.DateTimeField(auto_now_add=True)

    note              = models.ForeignKey(Note)
    
    owner             = models.ForeignKey('users.User')

    @classmethod
    def create(cls, query, owner, note):
        query = cls(query=query, owner=owner, note=note)
        return query
    
    class Meta:
        ordering = ('date_time_queried', )


class Source(models.Model):
    ''' Sources for DataPoints and Notes '''
    url            = models.CharField(max_length=255)
    found_date     = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    title          = models.CharField(max_length=30)

    def __str__(self):
        return self.url

    @classmethod
    def create(cls, url, title):
        source = cls(url=url, title=title)
        return source

    def add_tag(self, tag):
        self.tags.add(tag)

        

class Tag(models.Model):
    ''' Tagging for Notes, DataPoints and Sources '''
    tag           = models.CharField(max_length=16)
    creation_date = models.DateTimeField(auto_now_add=True)

    notes         = models.ManyToManyField(Note)
    data_points   = models.ManyToManyField(DataPoint)
    sources       = models.ManyToManyField(Source)
    
    def __str__(self):
        return tag

    @classmethod
    def create(cls, tag):
        return cls(tag=tag)

        
    
    
