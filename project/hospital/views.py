from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, r'index.html', context={'title': 'Hello Django'})

def ico(request):
    return HttpResponse(open(r'hospital\templates\ico\logo.png', 'rb').read(), content_type='image/jpg')
    