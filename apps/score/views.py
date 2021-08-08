from django.shortcuts import render, HttpResponse
from .models import *
from apps.index.models import *
import json

# Create your views here.

DATA = {
    'match': {
        'event': '',
        'eventName': '',
        'id': '',
        'type': 0,
        'serial': 0,
        'mode': '',
        'team': [],
        'leftTime': 0,
        'passTime': 0,
    },
    'score': {
        'blue': {
            'each': [],
            'auto_a': 0,
            'auto_c': 0,
            'tele_a': 0,
            'tele_c': 0,
            'end_c': 0,
            'foul': 0,
            'tech': 0,
            'all': 0,
        },
        'red': {
            'each': [],
            'auto_a': 0,
            'auto_c': 0,
            'tele_a': 0,
            'tele_c': 0,
            'end_c': 0,
            'foul': 0,
            'tech': 0,
            'all': 0,
        },
    }
}

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
    
def referee(request):
    return render(request, 'match/referee.html')

def data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
    else:
        return HttpResponse(json.dumps(DATA))
