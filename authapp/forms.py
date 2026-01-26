from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from authapp.models import Profile

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"class":"w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
        })
    )
    
    phone = forms.CharField(
    max_length=15,
    widget=forms.TextInput(attrs={
        "class": "w-full px-4 py-2 border-2 border-gray-500 rounded-md",
        "type": "tel",
        "autocomplete": "tel",
        "inputmode": "numeric",
        "pattern": "[0-9]{10}",
        "placeholder": "Enter phone number"
    })
)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
        })
    )
    class Meta:
        model = User
        fields=["username","email","phone","password1","password2"]
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "phone"]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-200",
                "placeholder": "Enter full name"
            }),
            "phone": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:ring focus:ring-indigo-200",
                "placeholder": "Enter phone number"
            }),
        }                                         