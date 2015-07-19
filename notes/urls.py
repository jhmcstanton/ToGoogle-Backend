from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.test_view, name='test_view'),
    #url(r'^$', views.handle_note, name='handle_note_view'),
    url(r'^$', views.list_notes, name='list_notes_view'),
    url(r'^single/', views.single_note, name='read_single_note_view'),
    url(r'^update_note/', views.update_single_note, name='update_single_note_view'),
    url(r'^find_similar/', views.find_similar, name='find_similar_values_view'),
]
