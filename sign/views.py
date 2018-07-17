from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request,"index.html")

#登录
def login_action(request):
    if request.method=="POST":
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user) #登录
            #对路径进行重定向，从而将登录成功后的请求指向/event_manage目录
            response=HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user',username,3600)  #添加浏览器cookie
            request.session['user']=username  #将session 信息记录在浏览器中
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

#发布会管理
#限制此函数必须登录才能访问，加上装饰函数
@login_required
def event_manage(request):
    #username=request.COOKIES.get('user' ,'')  #读取浏览器cookie
    username=request.session.get('user','') #读取浏览器session
    return  render(request,'event_manage.html',{"user":username})