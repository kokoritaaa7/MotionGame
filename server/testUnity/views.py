from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'testUnity/home.html')

def prac(request):
    return render(request, 'testUnity/prac.html')