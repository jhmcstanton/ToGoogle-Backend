from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.test_view, name='test_view'),
    url(r'^$', views.handle_note, name='handle_note_view'),
]
