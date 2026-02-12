from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.topic_list, name='topic_list'),
  #  path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
]