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
        'team': ['', '', '', ''],
        'leftTime': 0,
        'passTime': 0,
        'yellow': [0, 0, 0, 0],
        'red': [0, 0, 0, 0],
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
    return render(request, 'match/control.html', {
        'eventList': Event.objects.all(),
        'data': DATA,
    })

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
        if data['cmd'] == 'changeEvent':
            event = Event.objects.get(id=data['event'])
            matchList = [{'name': f'{m.type.name} {m.serial}', 'id': m.id} for m in event.match_set.all()]
            teamList = [{'id': int(t.id), 'name': t.name} for t in event.team.all()]
            res = {'matchList': matchList, 'teamList': teamList}

            DATA['match']['event'] = data['event']
            DATA['match']['eventName'] = event.name

        elif data['cmd'] == 'changeMatch':
            match = Match.objects.get(id=data['match'])
            team = [int(mt) for mt in match.team.split(',')]
            res = {'team': team}

            DATA['match']['id'] = data['match']
            DATA['match']['type'] = match.type.id
            DATA['match']['serial'] = match.serial
            DATA['match']['team'] = match.team.split(',')
        elif data['cmd'] == 'changeTeam':
            print(data)
            t = ''
            match = Match.objects.get(id=DATA['match']['id'])
            for tmp in data['team']:
                t = t + str(tmp) + (',' if tmp != data['team'][-1] else '')
            match.team = t
            match.save()
            res = {'res': 'ok'}
            
            DATA['match']['team'] = data['team']

        elif data['cmd'] == 'time':
            DATA['match']['mode'] = data['mode']
            DATA['match']['passTime'] = data['passTime']
            DATA['match']['leftTime'] = data['leftTime']
            res = {'res': 'ok'}

        elif data['cmd'] == 'reset':
            DATA['match']['mode'] = 0
            DATA['match']['passTime'] = 0
            DATA['match']['leftTime'] = 0
            res = {'res': 'ok'}

        return HttpResponse(json.dumps(res))

    else:
        return HttpResponse(json.dumps(DATA))
