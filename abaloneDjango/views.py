from random import random, randint

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .forms import UserLoginForm, KnightSelectForm
from .models import Board, Knight, User, SelectKnight
from .serializers import RegistrationUserSerializer


def knight_select_view(request, username):
    template_name = 'abaloneDjango/knight_select.html'
    #print('11111')
    if request.method == 'POST':
        form = KnightSelectForm(request.POST)
        #print ('2222')

        username = request.POST.get('username')

        user, created = User.objects.get_or_create(
            username=username
        )

        user.username = username
        user.readyYn = 'Y'
        user.joinYn = 'Y'

        user.save()

        delSelectKnightList = SelectKnight.objects.filter(username=username)

        delSelectKnightList.delete()

        knightliststr = request.POST.get('knightliststr')

        #print('2222'+knightliststr+'2222')

        knightlist = knightliststr.split(';')

        for knightId in knightlist :
            #print(knightId)
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
        knightlist = Knight.objects.filter(~Q(knightId=9)).order_by('knightId')
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

    context = {
        'userlist': userlist,  # 추가
        'joinusercnt': joinusercnt,  # 추가
        'readyusercnt': readyusercnt,  # 추가
    }
    return render(request, template_name, context)


def assin_view(request):
    template_name = 'abaloneDjango/start.html'
    weight = 3
    assinnum = 0
    userlist = User.objects.filter(joinYn='Y')

    for user in userlist:
        user.assinKnightId = 0
        user.save()

    joinusercnt = User.objects.filter(joinYn='Y').count()

    assineduserq = Q()
    for i in range(1,joinusercnt+1):

        q = Q(knightId=i)
        q.add(~assineduserq ,q.AND)
        #print('index::::' + i.__str__()+ '::'+ q.__str__())

        selectknightlist = SelectKnight.objects.filter(q)

        #for selectknight in selectknightlist:
            #print(selectknight.username + selectknight.knightId.__str__() )

        selectknightcnt = weight * selectknightlist.count()

        assinnum = randint(1,joinusercnt + selectknightcnt +1 - i)
        #print('index::::' + i.__str__() + '::assinnum:'+ assinnum.__str__()+ '::selectknightcnt:'+ selectknightcnt.__str__()+ '::joinusercnt:'+ joinusercnt.__str__()+ ':::'+ ( ((assinnum-1)/3).__int__()+1).__str__())

        if assinnum <= selectknightcnt:
            #print('111::(assinnum - selectknightcnt-1):' + ( (assinnum-1)/weight).__int__().__str__())
            assinedusername = selectknightlist[ ( (assinnum-1)/weight).__int__()].username
            #print('111:' + selectknightlist.__str__())

        else:
            unassineduserlist = User.objects.filter(Q(joinYn='Y') & Q(assinKnightId=0))
            #print('222::(assinnum - selectknightcnt-1):' + (
            #            assinnum - selectknightcnt - 1).__str__())
            assinedusername = unassineduserlist[(assinnum - selectknightcnt-1)].username
            #print('222:' + assinedusername)

        user = get_object_or_404(User, username=assinedusername)
        user.assinKnightId = i
        user.save()

        assineduserq.add( Q(username=assinedusername) , assineduserq.OR)
        #print(assineduserq.__str__())

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


def init_view(request):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all()

    for user in userlist:
        user.joinYn = 'N'
        user.readyYn = 'N'
        user.assinKnightId = 0
        user.save()

    selectknightlist = SelectKnight.objects.all()

    for selectknight in selectknightlist:
        selectknight.delete()


    return HttpResponseRedirect('/start/')