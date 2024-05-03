from rest_framework import serializers
from Project.models import Podcast,Subscribe,BookRandall,Videos,Testimonial


class PodcastSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Podcast
        fields = ['podcast_image', 'full_name', 'youtube_url', 'apple_url', 'google_url', 'spotify_url', 'time_stamp', 'podcast_des']


class SubscribeSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Subscribe
        fields = '__all__'


class BookRandallSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRandall
        fields = '__all__'
              

class VideoSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Videos
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        
        




