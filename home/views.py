from django.core import paginator
from django.http import request
from django.http.request import host_validation_re
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
# import sys
# sys.path.append("D:/DATAbase/django_db/")
# from rbac import models



import pymysql

#DataFlair #Views #TemplateInheritance
# Create your views here.


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')  
        filterResult =User.objects.filter(username = username)
        if len(filterResult)>0:
            return render(request,'login/regi-fail.html',{'error':"用户名已存在"})
        else:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if (password2 != password1):
                return render(request,'login/regi-fail.html',{'error':"两次密码不一致"})
            #将表单写入数据库
            user = User.objects.create_user(username=username,password=password1)
            #返回注册成功页面
            return render(request,'login/success.html',{'operation':"注册"})
    return render(request,'login/register.html',)
    
def login(request):  
    if request.method == "POST":
            #获取表单信息
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = auth.authenticate(username=username,password=password)
            if user_obj:  
                auth.login(request,user_obj)  
                next_url = request.GET.get('next')    
                if next_url:
                    return redirect(next_url)  
                return render(request,'login/success2.html',{'operation':"登录"})
            else:
               return render(request,'login/login-fail.html',{'error':"用户名或密码错误"})
    return render(request,"login/login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def wrong(request):
    return render(request,'login/wrong.html')





