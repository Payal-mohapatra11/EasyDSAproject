from django.urls import path
from . import views  
from .views import feedback_view
urlpatterns = [
    path('feedback/', views.feedback_view, name='feedback'),
 
]