from django.shortcuts import render
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import * 

def index(request):
    return render(request,'song/index.html',)

def base(request):
    return render(request,'song/base.html',)




