from typing import ClassVar
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login , logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# models import 
from .models import User, Gender, Admin, Member

# Home View 
class HomeView(View):
    def get(self,request,*args,**kwargs):

        return render(request,'index.html')
    def post(self,request,*args,**kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin_check = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request,user)
            is_admin = User.objects.get(email = user)
            if is_admin.is_admin :
                return redirect('admin')
            else:
                return redirect('member')
        else:
            if not admin_check:
                messages.warning(request,'Sorry Your Email Didnot Match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request,'Sorry Your Password Didnot Match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# Logout view
class LogoutView(View):    
    @method_decorator(login_required(login_url='home'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        logout(request)
        return redirect('home')

# Dashboard 
class Dashboard(View):
    @method_decorator(login_required(login_url='home'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        return render(request,'dashboard/dashboard.html')

# user Register View 
class UserRegister(View):
    def get(self,request,*args,**kwargs):
        return render(request,'register.html')
    
    def post(self,request,*args,**kwargs):
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        check_mail = User.objects.filter(email=email)
        if check_mail:
            messages.warning(request,'Email Already Exits !!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        elif password != password2:
            messages.warning(request,'Password didn`t match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        else:
            auth_info ={
                'username':username,
                'email':email,
                'password':make_password(password)
            }
            user = User(**auth_info)
            user.is_admin = False 
            user.save()
        member_obj = Member(user=user,name=name)
        member_obj.save()
        messages.success(request,'Thanks For Signing \n Please Log In to Continue')
        return redirect('home')

# Admin Dashboard 
class AdminDashboard(View):


    def get(self,request):
        return render(request,'dashboard/admin.html')

# Admin Dashboard 
class MemberDashboard(View):
    @method_decorator(login_required(login_url='home'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        return render(request,'dashboard/member.html')