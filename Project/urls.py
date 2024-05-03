from django.urls import path
from Project.views import *


urlpatterns = [
    path('add_podcast/',CreatePodcastView.as_view(), name="podcast"),
    path('podcasts/', PodcastAPIView.as_view(), name='podcast-list'),
    path('update_podcast/<int:pk>', UpdatePodcastView.as_view(), name='update-podcast'),
    path('delete_podcast/<int:pk>', DeletePodcastView.as_view(),name="delete-podcast"),
    
    # Subscribe URL'S
    path('add_subscribe/',CreateSubscribeView.as_view(), name="subscribe"),
    path('subscribes/', SubscriberView.as_view(), name="subscribe-list"),
    path('delete_subscribe/<int:pk>', DeleteSubscribeView.as_view(), name="delete-subscribe"),
    
    # BookRandall  URL'S
    path('add_bookrandall/', CreateBookRandallView.as_view(),name="bookrandall"),
    path('bookrandalls/', BookRandallView.as_view(), name="bookrandall-list"),
    path('detele_bookrandall/<int:pk>', DeleteBookRandallView.as_view(), name="delete-bookrandall"),
    
    
    # Videos URL'S
    path('add_video/', CreateVideoView.as_view(), name="add_video"),
    path('videos/', VideosView.as_view(), name="video-list"),
    path('update_video/<int:pk>', UpdateVideoView.as_view(),name="update-video"),
    path('delete_video/<int:pk>', DeleteVideoView.as_view(), name="delete-video"),
    
    
    # Testimonial URL'S
    path('add_testimonial/',CreateTestimonialView.as_view(), name="add-testimonial"),
    path('testimonials/',TestimonialsView.as_view(), name="testimonial-list"),
    path('update_testimonial/<int:pk>', UpdateTestimonialView.as_view(), name="update-testimonial"),
    path('delete_testimonial/<int:pk>', DeleteTestimonialView.as_view(), name="delete-testimonial")
    
]
