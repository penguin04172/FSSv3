from django.shortcuts import render, HttpResponse
from .models import *
from apps.index.models import *
import json, requests

# Create your views here.

DATA = {
    'match': {
        'event': '',
        'eventName': '',
        'id': '',
        'type': 0,
        'serial': 0,
        'mode': 0,
        'team': ['', '', '', ''],
        'leftTime': 0,
        'passTime': 0,
        'yellow': [0, 0, 0, 0],
        'red': [False, False, False, False],
        'count': [False, False],
    },
    'score': {
        'blue': {
            'each': [{
                'init': False,
                'auto_end': False,
                'tele_end': False
            }, {
                'init': False,
                'auto_end': False,
                'tele_end': False
            }],
            'auto_a': 0,
            'auto_c': 0,
            'tele_a': 0,
            'tele_c': 0,
            'end_c': 0,
            'foul': 0,
            'tech': 0,
            'all_point': 0,
        },
        'red': {
            'each': [{
                'init': False,
                'auto_end': False,
                'tele_end': False
            }, {
                'init': False,
                'auto_end': False,
                'tele_end': False
            }],
            'auto_a': 0,
            'auto_c': 0,
            'tele_a': 0,
            'tele_c': 0,
            'end_c': 0,
            'foul': 0,
            'tech': 0,
            'all_point': 0,
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

def prepare(request):
    teamList = [Team.objects.get(id=int(t)) for t in DATA['match']['team']]
    rank = json.loads(requests.get(f'http://127.0.0.1/rank?event={DATA["match"]["event"]}').text)
    return render(request, 'match/prepare.html', {'data': DATA, 'team': teamList, 'type': MatchType.objects.get(id=DATA['match']['type'])})

def result(request):
    teamList = [Team.objects.get(id=int(t)) for t in DATA['match']['team']]
    scoreBlue = {
        'all_point': DATA['score']['blue']['all_point'],
        'foul_point': DATA['score']['blue']['foul'] *5 + DATA['score']['blue']['tech'] *15,
        'init_point': (5 if DATA['score']['blue']['each'][0]['init'] else 0) + (5 if DATA['score']['blue']['each'][1]['init'] else 0),
        'end_point': (10 if DATA['score']['blue']['each'][0]['tele_end'] else 0) + (10 if DATA['score']['blue']['each'][1]['tele_end'] else 0) + (5 if DATA['score']['blue']['each'][0]['auto_end'] else 0) + (5 if DATA['score']['blue']['each'][1]['auto_end'] else 0) + DATA['score']['blue']['end_c']*10,
        'rank_point': (2 if DATA['score']['blue']['all_point'] > DATA['score']['red']['all_point'] else 0) + (1 if DATA['score']['blue']['auto_a'] + DATA['score']['blue']['tele_a'] >= 9 else 0) + (1 if DATA['score']['blue']['each'][0]['tele_end'] and DATA['score']['blue']['each'][1]['tele_end'] and DATA['score']['blue']['end_c'] > 0 else 0),
        'charged': DATA['score']['blue']['auto_a'] + DATA['score']['blue']['tele_a'] >= 9,
        'parked': DATA['score']['blue']['each'][0]['tele_end'] and DATA['score']['blue']['each'][1]['tele_end'] and DATA['score']['blue']['end_c'] > 0,
        'area_a': DATA['score']['blue']['auto_a']*15 + DATA['score']['blue']['tele_a']*7,
        'area_c': DATA['score']['blue']['auto_c']*5 + DATA['score']['blue']['tele_c'],
    }
    scoreRed = {
        'all_point': DATA['score']['red']['all_point'],
        'foul_point': DATA['score']['red']['foul'] *5 + DATA['score']['red']['tech'] *15,
        'init_point': (5 if DATA['score']['red']['each'][0]['init'] else 0) + (5 if DATA['score']['red']['each'][1]['init'] else 0),
        'end_point': (10 if DATA['score']['red']['each'][0]['tele_end'] else 0) + (10 if DATA['score']['red']['each'][1]['tele_end'] else 0) + (5 if DATA['score']['red']['each'][0]['auto_end'] else 0) + (5 if DATA['score']['red']['each'][1]['auto_end'] else 0) + DATA['score']['red']['end_c']*10,
        'rank_point': (2 if DATA['score']['red']['all_point'] > DATA['score']['blue']['all_point'] else 0) + (1 if DATA['score']['red']['auto_a'] + DATA['score']['red']['tele_a'] >= 9 else 0) + (1 if DATA['score']['red']['each'][0]['tele_end'] and DATA['score']['red']['each'][1]['tele_end'] and DATA['score']['red']['end_c'] > 0 else 0),
        'charged': DATA['score']['red']['auto_a'] + DATA['score']['red']['tele_a'] >= 9,
        'parked': DATA['score']['red']['each'][0]['tele_end'] and DATA['score']['red']['each'][1]['tele_end'] and DATA['score']['red']['end_c'] > 0,
        'area_a': DATA['score']['red']['auto_a']*15 + DATA['score']['red']['tele_a']*7,
        'area_c': DATA['score']['red']['auto_c']*5 + DATA['score']['red']['tele_c'],
    }
    return render(request, 'match/result.html', {
        'data': DATA, 'team': teamList,
        'type': MatchType.objects.get(id=DATA['match']['type']),
        'scoreBlue': scoreBlue,
        'scoreRed': scoreRed,
    })

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
            blue = match.score_set.first()
            red = match.score_set.last()
            team = [int(mt) for mt in match.team.split(',')]
            res = {'team': team}

            DATA['match']['id'] = data['match']
            DATA['match']['type'] = match.type.id
            DATA['match']['serial'] = match.serial
            DATA['match']['team'] = match.team.split(',')
            
            DATA['score']['blue']['each'][0]['init'] = blue.each_set.first().init
            DATA['score']['blue']['each'][0]['auto_end'] = blue.each_set.first().auto_end
            DATA['score']['blue']['each'][0]['tele_end'] = blue.each_set.first().tele_end
            DATA['score']['blue']['each'][1]['init'] = blue.each_set.last().init
            DATA['score']['blue']['each'][1]['auto_end'] = blue.each_set.last().auto_end
            DATA['score']['blue']['each'][1]['tele_end'] = blue.each_set.last().tele_end
            DATA['score']['blue']['auto_a'] = blue.auto_a
            DATA['score']['blue']['auto_c'] = blue.auto_c
            DATA['score']['blue']['tele_a'] = blue.tele_a
            DATA['score']['blue']['tele_c'] = blue.tele_c
            DATA['score']['blue']['end_c'] = blue.end_c
            DATA['score']['blue']['foul'] = blue.foul
            DATA['score']['blue']['tech'] = blue.tech
            DATA['score']['blue']['all_point'] = blue.all_point
            
            DATA['score']['red']['each'][0]['init'] = red.each_set.first().init
            DATA['score']['red']['each'][0]['auto_end'] = red.each_set.first().auto_end
            DATA['score']['red']['each'][0]['tele_end'] = red.each_set.first().tele_end
            DATA['score']['red']['each'][1]['init'] = red.each_set.last().init
            DATA['score']['red']['each'][1]['auto_end'] = red.each_set.last().auto_end
            DATA['score']['red']['each'][1]['tele_end'] = red.each_set.last().tele_end
            DATA['score']['red']['auto_a'] = red.auto_a
            DATA['score']['red']['auto_c'] = red.auto_c
            DATA['score']['red']['tele_a'] = red.tele_a
            DATA['score']['red']['tele_c'] = red.tele_c
            DATA['score']['red']['end_c'] = red.end_c
            DATA['score']['red']['foul'] = red.foul
            DATA['score']['red']['tech'] = red.tech
            DATA['score']['red']['all_point'] = red.all_point
            
            DATA['match']['yellow'] = [0, 0, 0, 0]
            DATA['match']['red'] = [False, False, False, False]

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
            match = Match.objects.get(id=DATA['match']['id'])
            match.played = True
            match.save()

            score = match.score_set.all()
            b1 = score.first().each_set.first()
            b1.__dict__.update(**DATA['score']['blue']['each'][0])
            b1.save()
            b2 = score.first().each_set.last()
            b2.__dict__.update(**DATA['score']['blue']['each'][1])
            b2.save()
            blue = score.first()
            blue.auto_a = DATA['score']['blue']['auto_a']
            blue.auto_c = DATA['score']['blue']['auto_c']
            blue.tele_a = DATA['score']['blue']['tele_a']
            blue.tele_c = DATA['score']['blue']['tele_c']
            blue.end_c = DATA['score']['blue']['end_c']
            blue.foul = DATA['score']['blue']['foul']
            blue.tech = DATA['score']['blue']['tech']
            blue.all_point = DATA['score']['blue']['all_point']
            blue.rank_point = (2 if DATA['score']['blue']['all_point'] > DATA['score']['red']['all_point'] else 0) + (1 if DATA['score']['blue']['auto_a'] + DATA['score']['blue']['tele_a'] >= 9 else 0) + (1 if DATA['score']['blue']['each'][0]['tele_end'] and DATA['score']['blue']['each'][1]['tele_end'] and DATA['score']['blue']['end_c'] > 0 else 0)
            blue.save()

            r1 = score.last().each_set.first()
            r1.__dict__.update(**DATA['score']['red']['each'][0])
            r1.save()
            r2 = score.last().each_set.last()
            r2.__dict__.update(**DATA['score']['red']['each'][1])
            r2.save()
            red = score.last()
            red.auto_a = DATA['score']['red']['auto_a']
            red.auto_c = DATA['score']['red']['auto_c']
            red.tele_a = DATA['score']['red']['tele_a']
            red.tele_c = DATA['score']['red']['tele_c']
            red.end_c = DATA['score']['red']['end_c']
            red.foul = DATA['score']['red']['foul']
            red.tech = DATA['score']['red']['tech']
            red.all_point = DATA['score']['red']['all_point']
            red.rank_point = (2 if DATA['score']['red']['all_point'] > DATA['score']['blue']['all_point'] else 0) + (1 if DATA['score']['red']['auto_a'] + DATA['score']['red']['tele_a'] >= 9 else 0) + (1 if DATA['score']['red']['each'][0]['tele_end'] and DATA['score']['red']['each'][1]['tele_end'] and DATA['score']['red']['end_c'] > 0 else 0)
            red.save()
            
            DATA['match']['mode'] = 0
            DATA['match']['passTime'] = 0
            DATA['match']['leftTime'] = 0
            DATA['match']['yellow'] = [0, 0, 0, 0]
            DATA['match']['red'] = [False, False, False, False]
            DATA['match']['count'] = [0, 0]
            res = {'res': 'ok'}

        elif data['cmd'] == "scoring":
            color = DATA['score'][data['blue']]
            if data['type'] == 'switch':
                if data['target'] == 'tele_c':
                    blue = (data['blue'] != 'blue')
                    DATA['match']['count'][blue] = not DATA['match']['count'][blue]
                else:
                    which = data['target'].split('-')
                    color['each'][int(which[1])-1][which[0]] = not color['each'][int(which[1])-1][which[0]]
            else:
                color[data['target']] = data['value']
            
            all = 0
            for e in DATA['score'][data['blue']]['each']:
                all = all + (5 if e['init'] else 0) + (5 if e['auto_end'] else 0) + (10 if e['tele_end'] else 0)
            all = all + color['auto_a']*15 + color['auto_c']*5
            all = all + color['tele_a']*7 + color['tele_c']
            all = all + color['end_c']*10
            all = all + color['foul']*5 + color['tech']*15
            color['all_point'] = all
            res = {'res': 'ok'}

        elif data['cmd'] == "referee":
            DATA['score'][data['side']][data['tar']] = data['num']
            res = {'res': 'ok'}

        elif data['cmd'] == 'warn':
            if data['type'] == 'warn':
                DATA['match']['yellow'][data['tar']] = DATA['match']['yellow'][data['tar']] + 1
                DATA['match']['red'][data['tar']] = DATA['match']['yellow'][data['tar']] >= 3
            elif data['type'] == 'out':
                DATA['match']['red'][data['tar']] = True
            res = {'res': 'ok'}
        
        else:
            res = {'res': 'cmdNotFound'}

        return HttpResponse(json.dumps(res))

    else:
        return HttpResponse(json.dumps(DATA))
