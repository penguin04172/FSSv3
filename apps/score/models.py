from django.db import models
from apps.index.models import *

# Create your models here.
class Score(models.Model):
    match = models.ForeignKey(Match, models.CASCADE)
    auto_a = models.IntegerField(default=0)
    auto_c = models.IntegerField(default=0)
    tele_a = models.IntegerField(default=0)
    tele_c = models.IntegerField(default=0)
    end_c = models.IntegerField(default=0)
    foul = models.IntegerField(default=0)
    tech = models.IntegerField(default=0)
    all_point = models.IntegerField(default=0)

class Each(models.Model):
    init = models.BooleanField(default=False)
    auto_end = models.BooleanField(default=False)
    tele_end = models.BooleanField(default=False)
    score = models.ForeignKey(Score, models.CASCADE)
