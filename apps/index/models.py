from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor

# Create your models here.
class Team(models.Model):
    id = models.DecimalField(max_digits=4, decimal_places=0, primary_key=True, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.id} {self.name}'
    class Meta:
        ordering = ['id']

class Event(models.Model):
    id = models.CharField(max_length=4, primary_key=True, unique=True)
    name = models.CharField(max_length=64)
    date = models.DateField()
    location = models.CharField(max_length=64, blank=True)
    team = models.ManyToManyField(Team)

    def __str__(self):
        return self.id
    class Meta:
        ordering = ['id']

class MatchType(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class Match(models.Model):
    id = models.CharField(max_length=128, primary_key=True, unique=True)
    event = models.ForeignKey(Event, models.CASCADE)
    team = models.TextField(default='', blank=True)
    type = models.ForeignKey(MatchType, models.CASCADE)
    serial = models.IntegerField()
    rankBlue = models.IntegerField(default=0)
    rankRed = models.IntegerField(default=0)
    played = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.event.id} {self.type} {self.serial}'
    class Meta:
        ordering = ['event_id', 'type', 'serial']