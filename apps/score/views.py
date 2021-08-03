from django.shortcuts import render, HttpResponse
from .models import *
from apps.index.models import *

# Create your views here.
def control(request):
    return render(request, 'match/control.html')

def scoring(request):
    blue = request.GET.get('blue')
    return render(request, 'match/scoring.html', {
        'blue': blue,
    })

def stream(request):
    return render(request, 'match/stream.html')

def board(request):
    return render(request, 'match/scoreBoard.html')

def data(request):
    pass