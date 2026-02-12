from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Feedback

def feedback_view(request):
    if request.method=="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        domain = request.POST.get("domain")
        rating = request.POST.get("rating")
        issue_type = request.POST.get("issue_type")
        suggestions = request.POST.get("suggestions")
        recommendation=request.POST.get("recommendation")
        
        if request.user.is_authenticated:
            user = request.user
        else:
            user=None
        
        Feedback.objects.create(
           user=user,
            name=name,
            email=email,
            domain=domain,
            rating=rating,
            issue_type=issue_type,
            suggestions=suggestions,
            recommendation=recommendation,
        )
        messages.success(request,"Thank you for your feedback!")
        return redirect("feedback")
    return render(request,"feedback/feedback.html")


