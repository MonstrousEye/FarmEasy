from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.handleSignup, name="handleSignup"),
    path('login',views.handleLogin, name="handleLogin"),
    path('contact',views.contact, name="contact"),
    path('logout',views.handleLogout, name="handleLogout"),
    path('about',views.about, name="about"),
    path('blog',views.blog, name="blog"),
    path('search',views.search, name="search"),
    
    
]
 