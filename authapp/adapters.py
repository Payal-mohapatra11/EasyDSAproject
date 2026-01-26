from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from authapp.models import Profile


class CustomAccountAdapter(DefaultAccountAdapter):
    pass
class NoPromptAccountAdapter(DefaultSocialAccountAdapter):
    """
    Handles:
    - New Google users → auto-create
    - Existing Google users → login
    - Manual users → LINK Google account if emails match
    """

    def pre_social_login(self, request, sociallogin):
        # If already linked, do nothing
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get("email")
        if not email:
            return

        # Use filter().first() — SAFE
        user = User.objects.filter(email=email).first()
        if user:
            sociallogin.connect(request, user)