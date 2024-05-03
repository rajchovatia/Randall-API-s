from django.contrib import admin
from Project.models import Podcast,Subscribe,BookRandall,Videos,Testimonial


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin) :
    list_display = ['id','podcast_image', 'full_name','youtube_url', 'apple_url', 'google_url', 'spotify_url', 'time_stamp', 'podcast_des']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin) :
    list_display = ['email','date']
    
    
@admin.register(BookRandall)
class BookRandall(admin.ModelAdmin) :
    list_display = ['id','first_name','last_name','email','subject','message','created_at']


@admin.register(Videos)
class VideoAdmin(admin.ModelAdmin) :
    list_display = ['title','video_file','thumbnails','date','video_url']
    

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin) :
    list_display = ['name','image','date','content']
    
    
    