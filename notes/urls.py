from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.test_view, name='test_view'),
    url(r'^save_note/', views.save_note, name='save_note_view'),
]
