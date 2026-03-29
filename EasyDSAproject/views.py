from django.http import HttpResponse 
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')
def visualizers(request):
    return render(request, 'visualizers.html')
def features(request):
    return render(request,'features.html')
def chatbotpage(request):
    return render(request,'chatbot.html')
def about(request):
    return render(request,'aboutus.html')
def objectives(request):
    return render(request,'objective.html')
def supporrt(request):
    return render(request,'support&help.html')
def dashboard(request):
    return render(request,'dashboard.html')