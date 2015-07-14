from django.contrib import admin

# Register your models here.
from .models import Note, DataPoint, SearchQuery, Source, Tag

admin.site.register(Note)
admin.site.register(DataPoint)
admin.site.register(SearchQuery)
admin.site.register(Source)
admin.site.register(Tag)
