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
                        s = s + t + (',' if t != team[-1] else '\n')
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
                        s = s + t + (',' if t != team[-1] else '\n')
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
                        team = team+e+(',' if e != each[5] else '\n')
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
    return render(request, 'event.html', {
        'event': event,
        'teamAll': teamAll,
        'teamList': teamList,
        'qualList': qualList,
        'praticeList': praticeList,
        'playoffList': playoffList,
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
