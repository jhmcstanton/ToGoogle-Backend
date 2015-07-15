from django.db import models

#to do:
class User(models.Model):
    '''Basic user model. Holds basic account infomation. Holds other user information such as notes. '''
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    notes = models.OneToMany(Note)

    def __str__(self):
        return self.title

