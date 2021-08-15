import json, requests
from django.shortcuts import redirect, render, HttpResponse
from .models import *
from apps.score.models import *

# Create your views here.
def index(request):
    eventList = list(Event.objects.all())
    teamList = list(Team.objects.all())
    return render(request, 'index.html', {
        'eventList': eventList,
        'teamList': teamList,
    })

def event(request):
    id = request.GET.get('id')
    if request.method == 'POST':
        if not id:
            id = request.POST.get('id')
            name = request.POST.get('name')
            date = request.POST.get('date')
            location = request.POST.get('location')
            try:
                event = Event.objects.create(id=id, name=name, date=date, location=location)
            except:
                event = Event.objects.get(id=id)
                event.name = name
                event.date = date
                event.location = location
                event.save()
            return redirect('/')
        else:
            event = Event.objects.get(id=id)
            cmd = request.POST.get('cmd')
            if cmd == 'team':
                teamId = request.POST.get('team')
                event = Event.objects.get(id=id)
                event.team.add(Team.objects.get(id=teamId))
            elif cmd == 'match':
                type = request.POST.get('type')
                serial = request.POST.get('serial')
                team = request.POST.getlist('team')
                try:
                    match = Match.objects.create(id=f'{event.id}_{type}_{serial}', event=event, type_id=type, serial=serial)
                    s = ''
                    for t in team:
                        s = s + t + (',' if t != team[-1] else '')
                    match.team = s
                    match.save()
                    scoreBlue = Score.objects.create(match=match)
                    scoreRed = Score.objects.create(match=match)
                    for i in range(0, 4):
                        Each.objects.create(score= scoreBlue if i < 2 else scoreRed)
                except:
                    match = Match.objects.get(id=f'{event.id}_{type}_{serial}')
                    s = ''
                    for t in team:
                        s = s + t + (',' if t != team[-1] else '')
                    match.team = s
                    match.save()
            elif cmd == 'delete':
                target = request.POST.get('target')
                code = request.POST.get('id')
                if target == 'match':
                    Match.objects.get(id=code).delete()
                elif target == 'team':
                    event.team.remove(code)
                    event.save()
            elif cmd == 'upload':
                chunks = request.FILES['upload'].chunks()
                chunkList = chunks.split('\n')
                for chunk in chunkList[1:-1]:
                    each = chunk.split(',')
                    team = ''
                    for e in each[2:6]:
                        team = team+e+(',' if e != each[5] else '')
                    try:
                        match = Match.objects.create(id=f'{event.id}_{each[0]}_{each[1]}', event=event, type_id=int(each[0]), serial=int(each[1]), team=team)
                    except:
                        match = Match.objects.get(id=f'{event.id}_{each[0]}_{each[1]}')
                        match.team = team
                        match.save()
                    
                
    try:
        event = Event.objects.get(id=id)
    except:
        return redirect('/')
    teamAll = Team.objects.all()
    teamList = list(event.team.all())
    qualList = Match.objects.filter(event=event, type_id=2)
    praticeList = Match.objects.filter(event=event, type_id=1)
    playoffList = Match.objects.filter(event=event, type_id__gt=2)
    rankList = json.loads(requests.get(f'http://127.0.0.1/rank?event={id}').text)
    return render(request, 'event.html', {
        'event': event,
        'teamAll': teamAll,
        'teamList': teamList,
        'qualList': qualList,
        'praticeList': praticeList,
        'playoffList': playoffList,
        'rankList': rankList,
    })

def team(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        try:
            team = Team.objects.create(id=id, name=name)
        except:
            team = Team.objects.get(id=id)
            team.name = name
            team.save()
        return redirect('/')

    id = request.GET.get('id')
    try:
        team = Team.objects.get(id=id)
    except:
        return redirect('/')
    return render(request, 'team.html', {
        'team': team,
    })

def rank(request):
    event = Event.objects.get(id=request.GET.get('event'))
    team = event.team.all()
    match = Match.objects.filter(played=True, type_id=2, event=event)

    rank = []
    for t in team:
        rank.append({'team': int(t.id), 'rp': 0, 'auto': 0, 'tele': 0, 'end': 0, 'num': 0, 'rs': 0})

    for r in rank:
        for m in match:
            blue_score = m.score_set.first()
            red_score = m.score_set.last()
            teamList = m.team.split(',')
            if str(r['team']) == teamList[0]:
                r['rp'] = r['rp'] + blue_score.rank_point
                r['auto'] = r['auto'] + (5 if blue_score.each_set.first().init else 0) + blue_score.auto_a *15 + blue_score.auto_c *5
                r['tele'] = r['tele'] + blue_score.tele_a *7 + blue_score.tele_c
                r['end'] = r['end'] + (5 if blue_score.each_set.first().auto_end else 0) + (10 if blue_score.each_set.first().tele_end else 0) + blue_score.end_c *10
                r['num'] = r['num'] + 1
                r['rs'] = r['rp'] / r['num']
            elif str(r['team']) == teamList[1]:
                r['rp'] = r['rp'] + blue_score.rank_point
                r['auto'] = r['auto'] + (5 if blue_score.each_set.last().init else 0) + blue_score.auto_a *15 + blue_score.auto_c *5
                r['tele'] = r['tele'] + blue_score.tele_a *7 + blue_score.tele_c
                r['end'] = r['end'] + (5 if blue_score.each_set.last().auto_end else 0) + (10 if blue_score.each_set.last().tele_end else 0) + blue_score.end_c *10
                r['num'] = r['num'] + 1
                r['rs'] = r['rp'] / r['num']
            elif str(r['team']) == teamList[2]:
                r['rp'] = r['rp'] + red_score.rank_point
                r['auto'] = r['auto'] + (5 if red_score.each_set.first().init else 0) + red_score.auto_a *15 + red_score.auto_c *5
                r['tele'] = r['tele'] + red_score.tele_a *7 + red_score.tele_c
                r['end'] = r['end'] + (5 if red_score.each_set.first().auto_end else 0) + (10 if red_score.each_set.first().tele_end else 0) + red_score.end_c *10
                r['num'] = r['num'] + 1
                r['rs'] = r['rp'] / r['num']
            elif str(r['team']) == teamList[3]:
                r['rp'] = r['rp'] + red_score.rank_point
                r['auto'] = r['auto'] + (5 if red_score.each_set.last().init else 0) + red_score.auto_a *15 + red_score.auto_c *5
                r['tele'] = r['tele'] + red_score.tele_a *7 + red_score.tele_c
                r['end'] = r['end'] + (5 if red_score.each_set.last().auto_end else 0) + (10 if red_score.each_set.last().tele_end else 0) + red_score.end_c *10
                r['num'] = r['num'] + 1
                r['rs'] = r['rp'] / r['num']
    # print(rank)
        
    rank = sorted(rank, key= lambda e:(-e.__getitem__('rs')))
    return HttpResponse(json.dumps(rank))

def rankView(request):
    rankList = json.loads(requests.get(f'http://127.0.0.1/rank?event={request.GET.get("event")}').text)
    return render(request, 'rank.html', {
        'rankList': rankList,
    })