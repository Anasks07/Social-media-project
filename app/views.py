from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.validators import validate_email
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.contrib import messages
from.models import *
# Create your views here.
def home(request):
    posts=Post.objects.all()
    context={
    'posts':posts,
    'username': request.user.username,
    
    }
    return render(request,'home.html',context)



#Code section for User authentication# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def user_register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'username already exists')
            return redirect('register')
        
        if len(password)<8:
            messages.error(request,'password length should aleast have 8 characters')
            return redirect('register')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request,'email is already taken')
            return redirect('register')
        try:
            validate_email(email)
        except Exception as e:
            messages.error(request,'invalid email ')
            
        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        
    return render(request,'register.html')   

@never_cache
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)   
             
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid credientials')
            return redirect('login')
    return render(request,'login.html')    


def user_logout(request):
    logout(request)
    return redirect('login')   
        

#section for post !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def post(request):
    if request.method=='POST':
        content=request.POST.get('content')
        image=request.FILES.get('image')
        
        if not content and not image:
            messages.error(request,'must add data')
            return redirect('post')

        post=Post(user=request.user,content=content,image=image)
        post.save()
        return redirect('profile_home')
    return render(request,'addpost.html')

def update_post(request,id):
    postquery=Post.objects.get(id=id)
    if request.method=='POST':
        content=request.POST.get('content')
        image=request.FILES.get('image')
        if content:
           postquery.content=content
        if image:
            postquery.image=image
        postquery.save()
        return redirect('home')
    context={
    'data':postquery
    }
    return render(request,'updatepost.html',context)    
                
    

def delete_post(request,id):
    post=Post.objects.get(id=id)
    post.delete()
    return redirect('profile_home')

@never_cache
def post_details(request,id):
    post= get_object_or_404(Post,id=id)
    comments=post.comments.all()
    context={
        'post':post,
        'comments':comments
    }
    return render(request,'post_details.html',context)

@never_cache
def add_comment(request,id):
    post=Post.objects.get(id=id)
    if request.method=="POST":
        content=request.POST.get('content')
        if content:
           Comment.objects.create(user=request.user,content=content,post=post)
           return redirect('post_details',id=id)
        else:
            return redirect('add_comment',id=id)
       
    return render(request,'comment.html',context={'post':post})    

def like_post(request,id):
    post=get_object_or_404(Post,id=id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    
    data={
        'liked':liked,
        'total_likes':post.likes.count(),
    }    
    return JsonResponse(data)
            

@never_cache
def delete_comment(request,id):
    comment = get_object_or_404(Comment, id=id)
    post_id=comment.post.id
    comment.delete()
    return redirect('post_details',id=post_id)


         
#user profile section !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def view_profile(request,username):
    user_name=get_object_or_404(User,username=username)    
    user_profile=get_object_or_404(Profile,user=user_name)
    posts=Post.objects.filter(user=user_name)
    if request.user.is_authenticated:
        is_following = user_profile in request.user.profile.following.all()
    else:
        is_following = False
        
    context={
        
        'user_profile':user_profile,
        'posts':posts,
        'is_following':is_following
    }            
    return render(request,'profile.html',context)

def profile_search_display(request):
    profile=User.objects.all()
    post = Post.objects.all()
    if 'search' in request.GET:
        search_obj=request.GET.get('search')
        if search_obj:
            profile_obj=profile.filter(username__icontains=search_obj)
            post_obj = post.filter(content__icontains=search_obj)
        else:
            return redirect('home')    
                
    else:
        messages.error(request,'Not found')
        return redirect('home')    
    context={
        'profile_obj':profile_obj,
        'post_obj':post_obj,
    }
    return render(request,'profile-search.html',context)    

def update_profile(request,id):
    user=get_object_or_404(User,id=id)
    profile_obj=get_object_or_404(Profile,user=user)
    if request.method=='POST':
        bio=request.POST.get('bio')
        image=request.FILES.get('image')
        
        if bio:
            profile_obj.bio=bio
        if image:
            profile_obj.user_image=image    
        profile_obj.save()
        return redirect('profiles',username=request.user.username)
    context={
        'profile_obj':profile_obj
    }
    return render(request,'updateprofile.html',context)    

def profile_follow(request,id):
   

    profile_to_follow=get_object_or_404(Profile,id=id)
    user_profile=get_object_or_404(Profile,user=request.user)
    
    if profile_to_follow in user_profile.following.all():
        user_profile.following.remove(profile_to_follow)
        is_following = False
    else:
        user_profile.following.add(profile_to_follow)
        is_following = True
    
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_following': is_following})
    else:
        return redirect('profiles', username=profile_to_follow.user.username)
    

def user_following(request,id):
    profile=get_object_or_404(Profile,id=id)
    profile_following=profile.following.all()
    context={
        'following':profile_following
    }
    return render(request,'following.html',context)


def user_followers(request,id):
    profile=get_object_or_404(Profile,id=id)
    profile_followers=profile.followers.all()
    context={
        'followers':profile_followers
    }
    return render(request,'follower.html',context)
        
# def user_following(request, id):
#     profile = get_object_or_404(Profile, id=id)
#     following_profiles = profile.following.all()
#     following_status = []

#     for following_profile in following_profiles:
#         is_following = request.user.profile.following.filter(id=following_profile.id).exists()
#         following_status.append({
#             'profile': following_profile,
#             'is_following': is_following
#         })
    
#     context = {
#         'following_status': following_status,
#         'profile': profile
#     }
#     return render(request, 'following.html', context)




