from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .forms import UserLoginForm
from .models import Board, Knight, User
from .serializers import RegistrationUserSerializer


def knight_select_view(request, username):
    template_name = 'abaloneDjango/knight_select.html'
    knightlist = Knight.objects.all()
    context = {
        'username':username,
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