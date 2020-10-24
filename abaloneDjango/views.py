from random import random, randint

from django.db.models import Q, Max, Count, FloatField
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .forms import UserLoginForm, KnightSelectForm, KnightElectionForm
from .models import Board, Knight, User, SelectKnight, Game, Election, Expedition, GameHistory
from .serializers import RegistrationUserSerializer


def knight_select_view(request, username):
    template_name = 'abaloneDjango/knight_select.html'

    if request.method == 'POST':
        form = KnightSelectForm(request.POST)

        username = request.POST.get('username')

        user, created = User.objects.get_or_create(
            username=username
        )

        user.username = username
        user.readyYn = 'Y'
        user.joinYn = 'Y'

        user.save()

        delSelectKnightList = SelectKnight.objects.filter(username=username)

        for delSelectKnight in delSelectKnightList:
            delSelectKnight.delete()

        knightliststr = request.POST.get('knightliststr')

        knightlist = knightliststr.split(';')

        for knightId in knightlist :
            if knightId == '':
                break

            selectKnight, created = SelectKnight.objects.get_or_create(
                username=username,
                knightId=knightId
            )
            selectKnight.save()

        return HttpResponseRedirect(
            '/mycard/%s' % username
        )

    else:
        form = KnightSelectForm()
        form.fields['username'].initial = username
        knightlist = Knight.objects.order_by('knightId')

        user, created = User.objects.get_or_create(
            username=username
        )
        user.username = username
        user.joinYn = 'Y'

        user.save()

        context = {
            'form': form,
            'username':username,
            'knightlist': knightlist,
        }

    return render(request, template_name, context)


def base_view(request):
    template_name = 'abaloneDjango/base.html'
    return render(request, template_name)


def knight_login_view(request):

    template_name = 'abaloneDjango/knight_login.html'

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():

            user, created = User.objects.get_or_create(
                username=form.cleaned_data['username']
            )

            user.username = form.cleaned_data['username']
            user.joinYn = 'Y'
            user.readyYn = 'N'

            user.save()

            return HttpResponseRedirect(
                '/knight_select/%s' % form.cleaned_data['username']
            )
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, template_name, context)


def knight_auto_view(request,username):
    user, created = User.objects.get_or_create(
        username=username
    )

    user.username = username
    user.joinYn = 'Y'
    user.readyYn = 'N'

    user.save()

    return HttpResponseRedirect(
        '/knight_select/%s' % username
    )


def mycard_view(request,username):

    template_name = 'abaloneDjango/mycard.html'

    user = get_object_or_404(User, username=username)

    if user.assinKnightId == 0:  # 미배정
        template_name = 'abaloneDjango/wait.html'

    joinusercnt = User.objects.filter(joinYn='Y').count()
    readyusercnt = User.objects.filter(readyYn='Y').count()

    cardinfo = ''
    cardinfostr = ''
    if user.assinKnightId == 1 : # 멀린

        userlist = User.objects.filter(assinKnightId__in=[6,7,10])

        for userinfo in userlist:
            cardinfostr = cardinfostr + '['+userinfo.username + '] '

        cardinfo = '모드레드를 제외한 악 : ' + cardinfostr
    elif user.assinKnightId == 2: # 퍼시발
        userlist = User.objects.filter(assinKnightId__in=[1,6])

        for userinfo in userlist:
            cardinfostr = cardinfostr + '[' + userinfo.username + '] '

        cardinfo = '멀린 or 모르가나 : '+ cardinfostr

    elif user.assinKnightId in [5,6,7]: # 모드레드
        userlist = User.objects.filter(assinKnightId__in=[5,6,7])

        for userinfo in userlist:
            cardinfostr = cardinfostr + '[' + userinfo.username + '] '

        cardinfo = '악의 하수인들 : '+ cardinfostr


    context = {
        'username': username,  # 추가
        'assinknightid': user.assinKnightId,  # 추가
        'cardinfo': cardinfo,  # 추가
        'joinusercnt': joinusercnt,  # 추가
        'readyusercnt': readyusercnt,  # 추가
    }

    return render(request, template_name, context)


def start_view(request):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all().order_by('-joinYn')  # 추가

    joinusercnt = User.objects.filter(joinYn='Y').count()

    readyusercnt = User.objects.filter(readyYn='Y').count()

    # 하나임
    gamelist = Game.objects.filter(completeYn='N')  # 추가

    context = {
        'userlist': userlist,  # 추가
        'joinusercnt': joinusercnt,  # 추가
        'readyusercnt': readyusercnt,  # 추가
        'gamelist':gamelist,
    }
    return render(request, template_name, context)


def assin_view(request):
    template_name = 'abaloneDjango/start.html'
    weight = 0
    assinnum = 0

    #참여 유저수
    joinusercnt = User.objects.filter(joinYn='Y').count()

    # 게임 setting
    gamecnt = Game.objects.filter(completeYn='N').count()

    if gamecnt > 0 :
        return render(request, 'abaloneDjango/error.html', {'errstr': '아직 진행중인 게임이 있습니다. 게임을 취소하고 다시 시도하십시오'} )

    gameIdObj = Game.objects.all().order_by('-gameId')

    if gameIdObj :
        gameId = gameIdObj[0].gameId + 1
    else:
        gameId= 1

    game = Game.objects.create()

    game.gameId = gameId
    game.joinUserCnt = joinusercnt
    
    #12명이 최대
    if game.joinUserCnt> 12 :
        game.joinUserCnt = 12
    

    game.save()


    # 카드 세팅 초기화
    userlist = User.objects.filter(joinYn='Y')

    for user in userlist:
        user.assinKnightId = 0
        user.save()


    # 카드 지정 완료 유저 Q
    assineduserq = Q()
    for i in range(1,joinusercnt+1):

        q = Q(knightId=i)
        q.add(~assineduserq ,q.AND)

        selectknightlist = SelectKnight.objects.filter(q)

        #for selectknight in selectknightlist:
            #print(selectknight.username + selectknight.knightId.__str__() )

        selectknightcnt = weight * selectknightlist.count()

        assinnum = randint(1,joinusercnt + selectknightcnt +1 - i)

        if assinnum <= selectknightcnt:
            assinedusername = selectknightlist[ ( (assinnum-1)/weight).__int__()].username

        else:
            unassineduserlist = User.objects.filter(Q(joinYn='Y') & Q(assinKnightId=0))
            assinedusername = unassineduserlist[(assinnum - selectknightcnt-1)].username

        user = get_object_or_404(User, username=assinedusername)
        user.assinKnightId = i
        user.save()

        assineduserq.add( Q(username=assinedusername) , assineduserq.OR)

    return HttpResponseRedirect('/start/' )


def delete_view(request,username):
    template_name = 'abaloneDjango/start.html'

    user = get_object_or_404(User, username=username)

    user.delete()

    return HttpResponseRedirect('/start/' )


def join_view(request,username):
    template_name = 'abaloneDjango/start.html'

    user = get_object_or_404(User, username=username)

    user.username = username
    user.joinYn = 'Y'

    user.save()

    return HttpResponseRedirect('/start/' )


def hosu_view(request,username):
    template_name = 'abaloneDjango/start.html'

    # 카드 세팅 초기화
    userlist = User.objects.filter(hosuYn='Y')

    for user in userlist:
        user.hosuYn = 'N'
        user.save()

    user = get_object_or_404(User, username=username)

    user.username = username
    user.hosuYn = 'Y'

    user.save()

    return HttpResponseRedirect('/start/' )


def init_view(request):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all()

    for user in userlist:
        user.joinYn = 'N'
        user.readyYn = 'N'
        user.hosuYn = 'N'
        user.assinKnightId = 0
        user.save()

    selectknightlist = SelectKnight.objects.all()

    for selectknight in selectknightlist:
        selectknight.delete()


    return HttpResponseRedirect('/start/')


def game_complete_view(request,gameid):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all()

    # 유저 지정카드 초기화
    for user in userlist:
        user.assinKnightId = 0
        user.save()

    game = get_object_or_404(Game, gameId=gameid)

    game.completeYn = 'Y'

    game.save()

    return HttpResponseRedirect('/start/' )


def game_succ_view(request,gameid):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.filter(joinYn='Y',assinKnightId__gt=0)

    # 유저 지정카드 초기화
    for user in userlist:
        # 투표검증

        knight = get_object_or_404(Knight, knightId=user.assinKnightId)
        if knight.evlYn == 'N':
            winYn = 'Y'         # 선
        else:
            winYn = 'N'

        gameHistory = GameHistory.objects.create()

        gameHistory.gameId = gameid
        gameHistory.succYn = 'Y'
        gameHistory.winYn = winYn
        gameHistory.username = user.username
        gameHistory.knightId = user.assinKnightId

        gameHistory.save()

    game = get_object_or_404(Game, gameId=gameid)

    game.completeYn = 'Y'

    game.save()

    return HttpResponseRedirect('/start/' )


def game_fail_view(request,gameid):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.filter(joinYn='Y')

    # 유저 지정카드 초기화
    for user in userlist:
        # 투표검증

        knight = get_object_or_404(Knight, knightId=user.assinKnightId)
        if knight.evlYn == 'Y':  # 악
            winYn = 'Y'
        else:
            winYn = 'N'

        gameHistory = GameHistory.objects.create()

        gameHistory.gameId = gameid
        gameHistory.succYn = 'N'
        gameHistory.winYn = winYn
        gameHistory.username = user.username
        gameHistory.knightId = user.assinKnightId

        gameHistory.save()

    game = get_object_or_404(Game, gameId=gameid)

    game.completeYn = 'Y'

    game.save()

    return HttpResponseRedirect('/start/' )


def expeditionSeq_ini_view(request,gameid):
    template_name = 'abaloneDjango/start.html'

    game = get_object_or_404(Game, gameId=gameid)
    expeditionSeq = game.expeditionSeq - 1
    if expeditionSeq < 1:
        expeditionSeq = 1

    game.expeditionSeq = expeditionSeq
    game.save()

    expedition = Expedition.objects.filter(gameId=gameid,expeditionSeq__gte=expeditionSeq)
    expedition.delete()

    election = Election.objects.filter(gameId=gameid, expeditionSeq__gte=expeditionSeq)
    election.delete()

    return HttpResponseRedirect('/start/' )


def knight_election_view(request, username):
    template_name = 'abaloneDjango/knight_election.html'

    gamemap = [
        [2, 3, 3, 4, 4],
        [2, 3, 3, 4, 4],
        [3, 4, 4, 5, 5],
        [3, 4, 4, 5, 5],
        [3, 4, 4, 5, 5],
        [4, 5, 5, 6, 6],
        [4, 5, 5, 6, 6],
    ]

    if request.method == 'POST':
        form = KnightElectionForm(request.POST)

        username = request.POST.get('username')
        gameid = request.POST.get('gameid')
        succyn = request.POST.get('succyn')
        expeditionseq = request.POST.get('expeditionseq')

        # 게임 및 회차 valid
        game = get_object_or_404(Game, gameId=gameid)
        if game.expeditionSeq.__str__()  != expeditionseq:
            return render(request, 'abaloneDjango/knight_error.html', {'username': username, 'errstr': '회차 오류/ 새로고침후 다시 투표'})
        if game.completeYn != 'N':
            return render(request, 'abaloneDjango/knight_error.html', {'username': username, 'errstr': '종료된 게임/ 새로고침후 다시 투표'})

        # 투표검증
        user = get_object_or_404(User, username=username)

        knight = get_object_or_404(Knight, knightId=user.assinKnightId)
        #print(knight.evlYn + succyn)
        if knight.evlYn == 'N' and succyn == 'N':
            return render(request, 'abaloneDjango/knight_error.html', {'username': username, 'errstr': '선은 실패를 낼 수 없습니다.'})

        # 투표여부확인
        electioncnt = Election.objects.filter(gameId=gameid, expeditionSeq=expeditionseq, username=username).count()

        if electioncnt > 0:
            return render(request, 'abaloneDjango/knight_error.html', {'username':username,'errstr': '이미 투표하셨습니다.'})

        election = Election.objects.create()

        election.gameId = gameid
        election.succYn = succyn
        election.expeditionSeq = expeditionseq
        election.username = username

        election.save()
        maxelectioncnt = gamemap[game.joinUserCnt-6][int(expeditionseq)-1]

        # 최종결과 저장
        electioncnt = Election.objects.filter(gameId=gameid,expeditionSeq=expeditionseq).count()
        if electioncnt >= maxelectioncnt:
            usernamelist = ''
            succcnt = Election.objects.filter(gameId=gameid, expeditionSeq=expeditionseq,succYn='Y').count()
            electionlist = Election.objects.filter(gameId=gameid, expeditionSeq=expeditionseq)

            for election in electionlist:
                usernamelist = usernamelist + '[' + election.username + ']'
            offset = 0
            
            # 4회차는 봐준다
            if expeditionseq == '4' :
                offset = 1

            if succcnt >= electioncnt - offset:
                expeditionsuccyn = 'Y'
            else:
                expeditionsuccyn = 'N'

            expedition = Expedition.objects.create()

            expedition.gameId = gameid
            expedition.expeditionSeq = expeditionseq
            expedition.succYn = expeditionsuccyn
            expedition.expeditionUserCnt = electioncnt
            expedition.succUserCnt = succcnt
            expedition.completeYn = 'Y'
            expedition.usernamelist = usernamelist

            expedition.save()

            # 진행회차 증가
            game.expeditionSeq = int(expeditionseq) + 1
            game.save()

        return HttpResponseRedirect(
            '/knight_expedition/%s' % username
        )

    else:
        form = KnightElectionForm()

        game = Game.objects.get(completeYn='N')

        if not game:  # 미배정
            return HttpResponseRedirect(
                '/mycard/%s' % username
            )
        form.fields['gameid'].initial = game.gameId
        form.fields['expeditionseq'].initial = game.expeditionSeq
        form.fields['username'].initial = username

        expeditionlist = Expedition.objects.filter(gameId=game.gameId).order_by('expeditionSeq')

        context = {
            'form': form,
            'username':username,
            'gameid': game.gameId,
            'joinusercnt': game.joinUserCnt,
            'expeditionseq': game.expeditionSeq,
            'expeditionlist': expeditionlist,
        }

    return render(request, template_name, context)


def knight_expedition_view(request, username):
    template_name = 'abaloneDjango/knight_expedition.html'

    if request.method == 'POST':
        template_name  = 'abaloneDjango/knight_election.html'

        form = KnightElectionForm(request.POST)

        username = request.POST.get('username')
        gameid = request.POST.get('gameid')
        succyn = request.POST.get('succyn')
        expeditionseq = request.POST.get('expeditionseq')

        form.fields['gameid'].initial = gameid
        form.fields['expeditionseq'].initial = expeditionseq
        form.fields['username'].initial = username
        form.fields['succyn'].initial = succyn

        # 투표여부확인
        electioncnt = Election.objects.filter(gameId=gameid, expeditionSeq=expeditionseq, username=username).count()

        if electioncnt > 0:
            return render(request, 'abaloneDjango/knight_error.html', {'username':username,'errstr': '이미 투표하셨습니다.'})

        return HttpResponseRedirect(
            '/knight_election/%s' % username
        )

    else:
        form = KnightElectionForm()

        try:
            game = Game.objects.get(completeYn='N')
        except Game.DoesNotExist:
            return HttpResponseRedirect(  '/mycard/%s' % username )

        form.fields['gameid'].initial = game.gameId
        form.fields['expeditionseq'].initial = game.expeditionSeq
        form.fields['username'].initial = username

        user = get_object_or_404(User, username=username)

        expeditionqslist = Expedition.objects.filter(gameId=game.gameId).order_by('expeditionSeq')

        expeditionlist = []
        expedition = {}

        for expeditionqs in expeditionqslist:
            expedition = expeditionqs.__dict__
            electionlist = []
            for i in range(0,expeditionqs.succUserCnt):
                electionlist.append('Y')
            for i in range(0, expeditionqs.expeditionUserCnt - expeditionqs.succUserCnt):
                electionlist.append('N')
            expedition['electionlist'] = electionlist

            expeditionlist.append(expedition)

        #print(expeditionlist)

        context = {
            'form': form,
            'username':username,
            'user':user,
            'gameid': game.gameId,
            'joinusercnt': game.joinUserCnt,
            'expeditionseq': game.expeditionSeq,
            'expeditionlist': expeditionlist,
        }

    return render(request, template_name, context)


def hosu_show_view(request, username):
    template_name = 'abaloneDjango/hosu.html'

    userlist = User.objects.filter(Q(joinYn='Y') & ~Q(username=username))  # 추가

    context = {
        'username':username,
        'userlist': userlist,  # 추가
    }
    return render(request, template_name, context)


def hosu_select_view(request, username):
    template_name = 'abaloneDjango/hosu_select.html'

     # 투증
    user = get_object_or_404(User, username=username)

    if user.hosuYn != 'Y' :
        return render(request, 'abaloneDjango/knight_error.html', {'username': username, 'errstr': '당신은 호수의 여신이 없습니다.'})

    targetusername = request.GET.get('target')

    print(targetusername)


    targetuser = get_object_or_404(User, username=targetusername)
    knight = get_object_or_404(Knight, knightId=targetuser.assinKnightId)

    targetuser.hosuYn = 'Y'
    targetuser.save()

    user.hosuYn = 'N'
    user.save()


    context = {
        'username': username,
        'targetusername':targetusername,
        'knight': knight,  # 추가
    }
    return render(request, template_name, context)


def honor_view(request, username):
    template_name = 'abaloneDjango/honor.html'

    honorlist = GameHistory.objects.values('username').annotate(totalcnt=Count('username')).annotate(wincnt=Count('username', Q(winYn='Y')))\
        .annotate(winrate=Cast('wincnt', output_field=FloatField())/Cast('totalcnt', output_field=FloatField()) * 100 ).order_by('-wincnt','-winrate')

    goodsucclist = GameHistory.objects.filter(knightId__in=[1,2]).values('username').annotate(totalcnt=Count('username')).annotate(wincnt=Count('username', Q(winYn='Y')))\
        .annotate(winrate=Cast('wincnt', output_field=FloatField())/Cast('totalcnt', output_field=FloatField()) * 100 ).order_by('-wincnt','-winrate')

    evlsucclist = GameHistory.objects.filter(knightId__in=[5,6,7,10]).values('username').annotate(totalcnt=Count('username')).annotate(wincnt=Count('username', Q(winYn='Y')))\
        .annotate(winrate=Cast('wincnt', output_field=FloatField())/Cast('totalcnt', output_field=FloatField()) * 100 ).order_by('-wincnt','-winrate')

    evlleaderlist = GameHistory.objects.filter(knightId__in=[5, 6]).values('username').annotate(
        totalcnt=Count('username')).annotate(wincnt=Count('username', Q(winYn='Y'))) \
        .annotate(
        winrate=Cast('wincnt', output_field=FloatField()) / Cast('totalcnt', output_field=FloatField()) * 100).order_by(
        '-wincnt', '-winrate')



    #print(honorlist)
    context = {
        'username':username,
        'honorlist': honorlist,  # 추가
        'goodsucclist': goodsucclist,  # 추가
        'evlleaderlist': evlleaderlist,  # 추가
        'evlsucclist': evlsucclist,  # 추가


    }
    return render(request, template_name, context)