from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Feedback(models.Model):
    DOMAIN_CHOICES=[
        ("1st Year Student","1st Year Student"),
        ("2nd Year Student","2nd Year Student"),
        ("3rd/4th Year Student","3rd Year Student"),
        ("Working Professional","Working Professional"),
        ("Beginner","Beginner"),
    ]
    RATING_CHOICES=[
        (5,"Excellent"),
        (4,"Very Good"),
        (3,"Good"),
        (2,"Average"),
        (1,"Poor"),
    ]
    RECOMMEND_CHOICES=[
        ("Definitely Yes","Definitely Yes"),
        ("Probably Yes","Probably Yes"),
        ("Maybe","Maybe"),
        ("Probably No","Probably No"),
        ("No","No"),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    domain=models.CharField(max_length=50,choices=DOMAIN_CHOICES)
    rating=models.IntegerField(choices=RATING_CHOICES)
    issue_type=models.CharField(max_length=100,blank=True)
    suggestions=models.TextField(blank=True)
    recommendation=models.CharField(max_length=50,choices=RECOMMEND_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}-{self.rating}"