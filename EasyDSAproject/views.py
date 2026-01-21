from django.http import HttpResponse 
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')
def visualizers(request):
    return render(request, 'visualizers.html')
def arrayvisualizers(request):
    return render(request, 'arrayvisualizers.html')
def linkedlistvisualizers(request):
    return render(request,'linkedlistvisualizer.html')
def chatbotpage(request):
    return render(request,'chatbot.html')