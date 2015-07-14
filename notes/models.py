from django.db import models

# Create your models here.
class Note(models.Model):
    ''' Basic note model for holding summaries and thoughts for users, as well as linking to DataPoints'''

    title               = models.CharField(max_length=30)
    summary             = models.TextField(max_length=255)
    creation_date_time  = models.DateTimeField(auto_now_add=True)
    last_edit_date_time = models.DateTimeField(auto_now=True)
    private             = models.BooleanField()
    
    ''' We probaby need owners and people allowed to view this at some point, which will likely require a
     DB migration or rebuild : 
    # owner =  models.ForeignKey('users.User')
    # reviewers = models.ManyToMany('users.User')
    '''    

    def __str__(self):
        return self.title

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

    ''' More user stuff for when we get there
    # owner = models.ForeignKey('users.User')
    # reviewers = models.ManyToMany('users.User')
    '''
    
    notes               = models.ManyToManyField(Note)

    def __str__(self):
        return self.datum

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
    
    '''
    More user stuff. We'll get there soon.
    # owner = models.ForeignKey('users.User')
    '''

    class Meta:
        ordering = ('date_time_queried', )
