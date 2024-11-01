from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    
    path('',home,name="home"),
    path('home',home,name="home"),
    path('post',post,name="post"),
    path('',view_profile,name="profile_home"),
    path('profile/<str:username>/',view_profile,name="profiles"),
    path('profile-search-display',profile_search_display,name="profiledisplay"),
    path('updateprofile/<int:id>/',update_profile,name="update_profile"),
    path('follow/<int:id>',profile_follow,name="profile_follow"),
    path('updatepost/<int:id>/',update_post,name="update_post"),
    path('delete-post/<int:id>/',delete_post,name="deletepost"),
    path('postdetails/<int:id>/',post_details,name="post_details"),
    path('addcomment/<int:id>/',add_comment,name="add_comment"),
    path('deletecomment/<int:id>/',delete_comment,name="delete_comment"),
    path('likepost/<int:id>/',like_post,name="like_post"),
    path('register',user_register,name="register"),
    path('login',user_login,name="login"),
    path('logout',user_logout,name="logout"),
    path('following/<int:id>/',user_following,name="following"),
    path('followers/<int:id>/',user_followers,name="followers"),

    
    

]