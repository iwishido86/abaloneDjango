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
    name = models.CharField(max_length=30)
    evlYn = models.CharField(max_length=1)
