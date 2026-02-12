from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from .models import Profile


# # Create or update Profile when user signs up or logs in
# @receiver(user_logged_in)
# def create_or_update_profile(sender, request, user, **kwargs):
#     profile, _ = Profile.objects.get_or_create(
#         user=user,
#         defaults={
#             "full_name": user.get_full_name() or user.username
#         }
#     )

#     # If login via Google, save Google data
#     social = user.socialaccount_set.filter(provider="google").first()
#     if social:
#         profile.gmailid = social.extra_data.get("email")
#         profile.avatar = social.extra_data.get("picture")
#         profile.save()
@receiver(social_account_added)
def save_google_profile(request, sociallogin, **kwargs):
    print("GOOGLE SIGNAL FIRED")  # Debug line

    user = sociallogin.user
    extra_data = sociallogin.account.extra_data

    profile, created = Profile.objects.get_or_create(user=user)

    profile.gmailid = extra_data.get("email")
    profile.avatar = extra_data.get("picture")
    profile.save()