import token
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import resend
from .forms import CustomResetForm, CustomSignupForm
from django.contrib.auth.models import User
from django.db.models import Q  #Q()-Query wrapper /Without Q, Django cannot combine conditions like that.
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.models import SocialAccount
from .models import Profile
from authapp.forms import ProfileEditForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm


#token_generator = PasswordResetTokenGenerator()
resend.api_key = settings.RESEND_API_KEY

# Create your views here.                      
def SignupView(request):
    #Auto-fill username and email if coming from google
    # google_email = request.session.get("google_email")
    # if request.method == "GET" and google_email:
    #      suggested_username = google_email.split("@")[0]
    #      base = suggested_username
    #      counter=1
    #      while User.objects.filter(username=suggested_username).exists():
    #          suggested_username = f"{base}{counter}"
    #          counter=counter+1
    #     #Prefill form with Google data
    #      form = CustomSignupForm(initial={"email":google_email,"username":suggested_username})
    #      return render(request,"authapp/signup.html",{"form":form})
    form = CustomSignupForm() 
         #Handle form submission   
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
              user=user,
        full_name=user.username,
        phone=form.cleaned_data.get("phone")
    )
            #  Check if user has Google account linked
            social_account = SocialAccount.objects.filter(user=user, provider="google").first()

            if social_account:
                profile.gmailid = social_account.extra_data.get("email")

            profile.save()
           
            
            
            return redirect("login")
    
    return render(request,"authapp/signup.html",{"form":form}) 


# 
def LoginView(request):
    """
    MANUAL LOGIN (Username/Email + Password)
    Google users are detected and handled safely
    """
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        
        if not username_or_email or not password:
            return render(request, "authapp/login.html", {
                "error": "Please enter both fields"
            })

        # Find user by username OR email
        user_qs = User.objects.filter(
            Q(username=username_or_email) | Q(email=username_or_email)
        )

        if not user_qs.exists():
            return render(request, "authapp/login.html", {
                "error": "User does not exist"
            })

        user_obj = user_qs.first()

        # IMPORTANT: Google users don't have passwords
        if not user_obj.has_usable_password():
            return render(request, "authapp/login.html", {
                "error": "This account uses Google login. Please login with Google or set a password."
            })

        # PASSWORD HASH CHECK HAPPENS HERE
        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user :
            login(request, user)
            return redirect("home")

        return render(request, "authapp/login.html", {
            "error": "Invalid password"
        })

    return render(request, "authapp/login.html")

@login_required
def success_view(request):
    return render(request, "authapp/success.html")

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.get_full_name() or request.user.username
        }
    )

    

    if request.user.email:
        profile.gmailid = request.user.email
        profile.save()

    return render(request, "authapp/profile.html", {
        "profile": profile
    })

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            new_username=form.cleaned_data.get("full_name")
            request.user.username = new_username
            request.user.save()
            profile.full_name=new_username
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "authapp/edit_profile.html", {
        "form": form
    })
    
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "Email not registered.")
            return redirect("forgot_password")

        user = users.first()   # get single user

        # If Google user
        if not user.has_usable_password():
            messages.error(request, "This account uses Google login.")
            return redirect("forgot_password")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = request.build_absolute_uri(
    reverse("reset_password", args=[uid, token])
)
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": "Reset Your Password",
            "text": f"Click the link below to reset your password:\n\n{reset_link}"
        })
        messages.success(request, "Reset link sent to your email.")

    return render(request, "authapp/forgot_password.html")

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if not user or not default_token_generator.check_token(user, token):
        messages.error(request, "Invalid or expired link.")
        return redirect("forgot_password")

    # Only create empty form on GET
    if request.method == "GET":
        form = CustomResetForm(user)
        return render(request, "authapp/reset_password.html", {"form": form})

    #  Only validate on POST
    if request.method == "POST":
        form = CustomResetForm(user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Password reset successful.")
            return redirect("login")

        # If invalid → render same form with errors
        return render(request, "authapp/reset_password.html", {"form": form})
