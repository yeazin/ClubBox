from django.urls import path
from django.views.generic.base import View
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(),name='logout'),

    path('admin/', views.AdminDashboard.as_view(),name='admin'),
    path('member/',views.MemberDashboard.as_view(),name='member'),
]
