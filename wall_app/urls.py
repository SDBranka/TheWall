from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_msg', views.add_msg),
    path('add_comment', views.add_comment),
    path('delete_msg', views.delete_msg),
]