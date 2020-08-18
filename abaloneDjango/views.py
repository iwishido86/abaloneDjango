from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .forms import UserLoginForm, KnightSelectForm
from .models import Board, Knight, User, SelectKnight
from .serializers import RegistrationUserSerializer


def knight_select_view(request, username):
    template_name = 'abaloneDjango/knight_select.html'
    print('11111')
    if request.method == 'POST':
        form = KnightSelectForm(request.POST)
        print ('2222')
        if form.is_valid():
            username = form.cleaned_data['username']

            user, created = User.objects.get_or_create(
                username=username
            )

            user.username = username
            user.readyYn = 'Y'

            user.save()

            delSelectKnightList = SelectKnight.objects.filter(username=username)

            delSelectKnightList.delete()

            knightliststr = form.cleaned_data['knightliststr']

            knightlist = knightliststr.split(';')

            for knightId in knightlist :
                print(knightId)
                if knightId == '':
                    break

                selectKnight, created = SelectKnight.objects.get_or_create(
                    username=form.cleaned_data['username'],
                    knightId=knightId
                )
                selectKnight.save()

            return HttpResponseRedirect(
                '/knight_select/%s' % username
            )

    else:
        form = KnightSelectForm()
        form.fields['username'].initial = username
        knightlist = Knight.objects.all()
        context = {
            'form': form,
            'knightlist': knightlist
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
            user.assinKnightId = 0

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

    user.save()

    return HttpResponseRedirect(
        '/knight_select/%s' % username
    )


def start_view(request):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all()  # 추가
    context = {
        'userlist': userlist  # 추가
    }
    return render(request, template_name, context)


def assin_view(request):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all()  # 추가
    context = {
        'userlist': userlist  # 추가
    }
    return HttpResponseRedirect(
        '/knight_select/%s'
    )


def delete_view(request):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all()  # 추가
    context = {
        'userlist': userlist  # 추가
    }
    return HttpResponseRedirect(
        '/knight_select/%s'
    )


def join_view(request):
    template_name = 'abaloneDjango/start.html'

    userlist = User.objects.all()  # 추가
    context = {
        'userlist': userlist  # 추가
    }
    return render(request, template_name, context)