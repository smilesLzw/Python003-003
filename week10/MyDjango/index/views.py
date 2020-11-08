from .form import LoginForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate


# Create your views here.
def index(request):
    return HttpResponse('Hello Django!')


def login1(request):
    # POST
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 读取表单的返回值
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user:
                # 登录用户
                login(request, user)
                return render(request, 'index.html')
            else:
                return HttpResponse('登录失败')
    # GET
    if request.method == 'GET':
        login_form = LoginForm()
        return render(
            request,
            'form.html',
            {'form': login_form},
        )
