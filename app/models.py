from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

 
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.CharField(max_length=280,blank=True)
    image=models.ImageField(upload_to="image",null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User,related_name='liked_posts',blank=True)
    retweet=models.ManyToManyField(User,related_name='retweetd_posts',blank=True)

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    post=models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
                      
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    user_image=models.ImageField(upload_to="profile_image",null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)
    bio=models.CharField(max_length=100,blank=True) 
    followers=models.ManyToManyField('self',symmetrical=False,related_name="following",blank=True)
    
    def __str__(self):
        return self.user.username    
    
    def following_count(self):
        return self.following.count()        
    
    def followers_count(self):
        return  self.followers.count()
    
    
    
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()          
    
    
            
    
    
    
