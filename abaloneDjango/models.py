# models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=False, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Board(models.Model):
    title = models.CharField(max_length=30)
    content_type = models.CharField(max_length=20)
    content = models.TextField()
    write_date = models.DateTimeField(auto_now_add=True)


class Knight(models.Model):
    knightId = models.IntegerField(default=0, help_text="카드번호",unique=True)
    name = models.CharField(max_length=30)
    evlYn = models.CharField(max_length=1)


class User(models.Model):
    username = models.CharField(max_length=30,unique=True)
    joinYn = models.CharField(max_length=1)
    readyYn = models.CharField(default='N',max_length=1)
    assinKnightId = models.IntegerField(default=0, help_text="지정카드")


class SelectKnight(models.Model):
    username = models.CharField(max_length=30)
    knightId = models.IntegerField(default=0, help_text="카드번호")



class User(models.Model):
    username = models.CharField(max_length=30,unique=True)
    joinYn = models.CharField(max_length=1)
    readyYn = models.CharField(default='N',max_length=1)
    assinKnightId = models.IntegerField(default=0, help_text="지정카드")


class Game(models.Model):
    gameId = models.IntegerField(default=0, help_text="원정번호")
    joinUserCnt = models.IntegerField(default=0, help_text="참여인수")
    expeditionSeq = models.IntegerField(default=1, help_text="진행중회차")
    completeYn = models.CharField(default='N', max_length=1)


class Expedition(models.Model):
    gameId = models.IntegerField(default=0, help_text="원정번호")
    expeditionSeq = models.IntegerField(default=0, help_text="원정회차")
    expeditionUserCnt = models.IntegerField(default=0, help_text="원정참여유저")
    succUserCnt = models.IntegerField(default=0, help_text="원정참여유저")
    succYn = models.CharField(default='N', max_length=1)
    completeYn = models.CharField(default='N', max_length=1)
    usernamelist = models.CharField(max_length=150)


class Election(models.Model):
    gameId = models.IntegerField(default=0, help_text="원정번호")
    expeditionSeq = models.IntegerField(default=0, help_text="원정회차")
    username = models.CharField(max_length=30)
    succYn = models.CharField(default='N', max_length=1)