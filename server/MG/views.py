from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def us(request):
    return render(request, 'MG/about-us.html')

def cart(request):
    return render(request, 'MG/cart.html')

def check(request):
    return render(request, 'MG/check-out.html')

def tact(request):
    return render(request, 'MG/contact.html')

def err(request):
    return render(request, 'MG/error.html')

def fea(request):
    return render(request, 'MG/features.html')

def ind(request):
    return render(request, 'MG/index.html ')

def log(request):
    return render(request, 'MG/login.html')

def pro(request):
    return render(request, 'MG/profile.html')

def ragist(request):
    return render(request, 'MG/registratio.html')

def shopdetail(request):
    return render(request, 'MG/shop-details.html')

def shop(request):
    return render(request, 'MG/shop.html')

def tourna(request):
    return render(request, 'MG/tournaments-single.html')

def tour(request):
    return render(request, 'MG/tournaments.html')

def tour_sing(request):
    return render(request, 'MG/tour_sing.html')

