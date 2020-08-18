# forms.py
from django import forms
from .models import Board


class BaseBulletinBoard(forms.ModelForm):
    class Meta:
        model = Board
        fields = '__all__'


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='이름',
        widget=forms.TextInput(attrs={'size': 30})

    )


class KnightSelectForm(forms.Form):
    username = forms.CharField(
        label='이름',
        widget=forms.HiddenInput(attrs={'size': 30}),
        #disabled=True
    )
    knightliststr = forms.CharField(
        label='선택기사목록',
        widget=forms.HiddenInput(attrs={'size': 30})
    )
