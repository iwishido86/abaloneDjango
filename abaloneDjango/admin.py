from django.contrib import admin

from .models import Board, User, SelectKnight, Election, Expedition, Game, GameHistory  # 추가
from .models import Knight   # 추가
# Register your models here.


class KnightAdmin(admin.ModelAdmin):
    list_display = ('knightId', 'name', 'evlYn',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'joinYn', 'readyYn', 'assinKnightId','hosuYn',)


class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('gameId', 'username','winYn','succYn', 'knightId',)


class GameAdmin(admin.ModelAdmin):
    list_display = ('gameId', 'joinUserCnt', 'expeditionSeq', 'completeYn',)


class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('gameId', 'expeditionSeq', 'expeditionUserCnt', 'succUserCnt', 'succYn', 'completeYn', 'usernamelist',)


admin.site.register(Knight,KnightAdmin)  # 추가
admin.site.register(Expedition,ExpeditionAdmin)  # 추가
admin.site.register(User,UserAdmin)  # 추가
admin.site.register(GameHistory,GameHistoryAdmin)  # 추가
admin.site.register(Game,GameAdmin)  # 추가
admin.site.register(SelectKnight)  # 추가
admin.site.register(Election)  # 추가