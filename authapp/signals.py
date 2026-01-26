from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from .models import Profile

# Create or update Profile when user signs up or logs in
@receiver(user_logged_in)
def create_or_update_profile(sender, request, user, **kwargs):
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            "full_name": user.get_full_name() or user.username
        }
    )

    # If login via Google, save Google data
    social = user.socialaccount_set.filter(provider="google").first()
    if social:
        profile.gmailid = social.extra_data.get("email")
        profile.avatar = social.extra_data.get("picture")
        profile.save()
