from django.urls import path

from . import views
from .views import SignupView, LoginView, logout_view, success_view,profile_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', SignupView, name="signup"),
    path('login/', LoginView, name="login"),
    path('logout/', logout_view, name="logout"),
   path("success/", success_view, name="success"),
    #  path("auth/delete/", delete_account, name="delete_account"),
    
     path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name="authapp/password_reset.html"
         ),
         name="password_reset"),
     path("profile/", profile_view, name="profile"),
     path("profile/edit/", views.edit_profile, name="edit_profile"),
]
