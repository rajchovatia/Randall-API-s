from django.db import models
# Create your models here.

class Podcast(models.Model) :
    podcast_image = models.ImageField(upload_to='podcast_images/', null=True, blank=True)
    full_name = models.CharField(max_length=240,null=True,blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    apple_url = models.URLField(null=True, blank=True)
    google_url = models.URLField(null=True, blank=True)
    spotify_url = models.URLField(null=True, blank=True)
    time_stamp = models.CharField(max_length=240, null=True, blank=True)
    podcast_des = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    
    
class Subscribe(models.Model) :
    email = models.EmailField(max_length=240,null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.email



class BookRandall(models.Model):
    first_name = models.CharField(max_length=240,null=True, blank=True)
    last_name = models.CharField(max_length=240,null=True, blank=True)
    email = models.EmailField(max_length=240,null=True, blank=True)
    subject = models.CharField(max_length=240,null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)



class Videos(models.Model) :
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    title = models.CharField(max_length=240,null=True, blank=True) 
    thumbnails = models.TextField(null=True, blank=True)
    date = models.CharField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)



class Testimonial(models.Model) :
    image = models.ImageField(upload_to='testimonial_image/', null=True, blank=True)
    name = models.CharField(max_length=240, null=True, blank=True)
    date = models.CharField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    

