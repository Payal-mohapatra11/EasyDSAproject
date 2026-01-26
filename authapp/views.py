from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from django.contrib.auth.models import User
from django.db.models import Q  #Q()-Query wrapper /Without Q, Django cannot combine conditions like that.
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.models import SocialAccount
from .models import Profile
from authapp.forms import ProfileEditForm
from django.contrib import messages
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
            
            profile, created = Profile.objects.get_or_create(
    user=user,
    defaults={
        "full_name": user.get_full_name() or user.username
    }
)
            profile.phone = form.cleaned_data.get("phone")
            google_email = request.session.get("google_email")
            if google_email:
                profile.gmailid = google_email
                del request.session["google_email"]

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
            return redirect("profile")

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

    return render(request, "authapp/profile.html", {
        "profile": profile
    })

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "authapp/edit_profile.html", {
        "form": form
    })