from django.shortcuts import render, redirect
from .models import User
from .forms import RegisterForm, LoginForm


# Create your views here.




# 회원 가입
def register(request):
    register_form = RegisterForm()
    nickname = request.session.get('nickname')
    context = {'forms': register_form, 'nickname': nickname}

    if request.method == 'GET':
        return render(request, 'accounts/register.html', context)
    elif request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            # 입력한 정보 저장
            user = User(
                user_id=register_form.user_id,
                nickname=register_form.nickname,
                user_pw=register_form.user_pw
            )
            user.save()
            nickname = request.session.get('nickname')
            context = {'forms': register_form, 'nickname': nickname}
            return render(request, 'property/index.html', context)
        else:
            context['forms'] = register_form
            if register_form.errors:
                for value in register_form.errors.values():
                    context['error'] = value
        return render(request, 'accounts/register.html', context)

# 로그인
def login(request):
    loginform = LoginForm()
    nickname = request.session.get('nickname')
    context = { 'forms': loginform, 'nickname': nickname }

    if request.method == 'GET':
        print("로그인 시작 겟방식")
        return render(request, 'accounts/login.html', context)
    elif request.method == 'POST':
        loginform = LoginForm(data=request.POST)
            # 로그인 폼 검증
        if loginform.is_valid():
            request.session['nickname']= loginform.nickname
            request.session.set_expiry(0)
            context = {}
            nickname = request.session.get('nickname', '')
            context = {'forms': loginform, 'nickname': nickname}
            print("포스트, 일반 로그인")
            #return render(request, 'property/index.html', context)
            return redirect('property:index')
        else:
            context['forms'] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'property/index.html', context)

# 로그아웃
def logout(request):
    request.session.flush()
    return redirect('property:index')

