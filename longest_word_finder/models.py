from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word = models.CharField(max_length=40)

    def __str__(self):
        return self.word


class ActionType(models.Model):
    name = models.CharField(max_length=25, unique=True)
    points_gained_per_action = models.IntegerField()

    def __str__(self):
        return self.name


class Action(models.Model):
    type = models.ForeignKey(ActionType)
    user = models.ForeignKey(User)
    word = models.ForeignKey(Word)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type.name


class Rank(models.Model):
    name = models.CharField(max_length=40, unique=True)
    points = models.IntegerField(verbose_name="Minimum Required Points")
    actions = models.ManyToManyField(ActionType)

    def __str__(self):
        return self.name


class Description(models.Model):
    description = models.CharField(max_length=256)
    word = models.OneToOneField(Word)

    def __str__(self):
        return "Description of the word: " + self.word.word
