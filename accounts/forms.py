from django import forms
from django.contrib.auth.models import User
from .models import User
from argon2 import PasswordHasher, exceptions
from django.shortcuts import render, redirect



class RegisterForm(forms.ModelForm):
    user_id = forms.CharField(
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'user_id',
                'id': 'user_id',
                'placeholder': '아이디'
            }
        ),
        error_messages={'required': '아이디를 입력하세요.', 'unique': '중복된 아이디 입니다.'}
    )
    user_pw = forms.CharField(
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'user_pw',
                'id': 'user_pw',
                'placeholder': '비밀번호'
            }
        ),
        error_messages={'required': '비밀번호를 입력하세요.'}
    )
    user_pw2 = forms.CharField(
        label='비밀번호 확인',
        required='True',
        widget=forms.PasswordInput(
            attrs={
                'class': 'user_pw2',
                'id': 'user_pw2',
                'placeholder': '비밀번호 확인'
            }
        ),
        error_messages={'required': '비밀번호가 일치하지 않습니다.'}
    )
    nickname = forms.CharField(
        label='닉네임',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'nickname',
                'id': 'nickname',
                'placeholder': '닉네임'
            }
        ),
        error_messages={'required': '닉네임을 입력하세요.'}
    )
    field_order = [
        'user_id',
        'nickname',
        'user_pw',
        'user_pw2'
    ]
    class Meta:
        model = User
        fields = [
            'user_id',
            'nickname',
            'user_pw'
        ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id', '')
        nickname = cleaned_data.get('nickname', '')
        user_pw = cleaned_data.get('user_pw', '')
        user_pw2 = cleaned_data.get('user_pw2', '')

        if user_pw != user_pw2:
            print("비번 틀림")
            return self.add_error('user_pw2', '비밀번호가 다릅니다.')
        elif 4 > len(user_id) or len(user_id) > 16:
            return self.add_error('user_id', '아이디는 4~16글자로 입력하세요.')
        elif 4 > len(user_pw):
            return self.add_error('user_pw', '비밀번호는 4자 이상으로 적어주세요')
        else:
            self.user_id = user_id
            self.nickname = nickname
            self.user_pw = PasswordHasher().hash(user_pw)
            self.user_pw2 = user_pw2


class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32,
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'user_id',
                'placeholder': '아이디'
            }
        ),
        error_messages={'required': '아이디를 입력하세요.'}
    )
    user_pw = forms.CharField(
        max_length=128,
        label='비밀빈호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'user_pw',
                'placeholder': '비밀번호'
            }
        ),
        error_messages={'required': '비밀번호를 입력하세요.'}
    )

    field_order = [
        'user_id',
        'user_pw',
    ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id', '')
        user_pw = cleaned_data.get('user_pw', '')

        if user_id == '':
            return self.add_error('user_id', '아이디를 다시 입력 하세요.')
        elif user_pw == '':
            return self.add_error('user_id', '비밀번호를 다시 입력 하세요.')
        else:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return self.add_error('user_id', '아이디가 다릅니다.')

            try:
                PasswordHasher().verify(user.user_pw, user_pw)
            except exceptions.VerifyMismatchError:
                return self.add_error('user_pw', '비밀번호가 다릅니다.')
            self.nickname = user.nickname


