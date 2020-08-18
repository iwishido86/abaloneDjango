from django.contrib import admin

from .models import Board, User, SelectKnight  # 추가
from .models import Knight   # 추가
# Register your models here.

admin.site.register(Board)  # 추가
admin.site.register(Knight)  # 추가
admin.site.register(User)  # 추가
admin.site.register(SelectKnight)  # 추가