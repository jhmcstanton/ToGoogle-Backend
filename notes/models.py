from django.db import models

# Create your models here.
class Note(models.Model):
    ''' Basic note model for holding summaries and thoughts for users, as well as linking to DataPoints'''

    title               = models.CharField(max_length=30)
    summary             = models.TextField(max_length=500)
    creation_date_time  = models.DateTimeField(auto_now_add=True)
    last_edit_date_time = models.DateTimeField(auto_now=True)
    private             = models.BooleanField()
    
    ''' We probaby need owners and people allowed to view this at some point, which will likely require a
     DB migration or rebuild : 
    # owner =  models.ForeignKey(User)
    # reviewers = models.ManyToMany(User)
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

    notes               = models.ManyToManyField(Note)

    def __str__(self):
        return self.datum

    class Meta:
        ordering = ('last_edit_date_time', 'creation_date_time', )
