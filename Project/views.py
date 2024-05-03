from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from Project.serializers import *
from Project.models import *
from helper.email_regex import validate_email
from django.db.models import Q
from Authentication.jwt_auth import CustomJWTAuthentication

# Podcast API  (COMPLETE)
class CreatePodcastView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def post(self, request) :
        try :
            serializer = PodcastSerializer(data = request.data)
            if serializer.is_valid() :   
                if not serializer.validated_data.get('podcast_image'):
                    return Response({'status': False, 'message': 'Profile image is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.validated_data.get('full_name'):
                    return Response({'status': False, 'message': 'Full name is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.validated_data.get('time_stamp'):
                    return Response({'status': False, 'message': 'Timestamp is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.validated_data.get('podcast_des'):
                    return Response({'status': False, 'message': 'Podcast description is required'}, status=status.HTTP_400_BAD_REQUEST)
                # Create the Podcast object
                serializer.save()
                return Response({'status' : True, 'message' : 'Podcast created successfully'}, status=status.HTTP_201_CREATED)
            else :
                errors = serializer.errors
                return Response({'status' : False, 'message' : 'Invalid data', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             return Response({'status':False,'message':f'Error - {e}'},status=status.HTTP_400_BAD_REQUEST)   
         

class PodcastAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    def get(self, request):
        try:
            # Get parameters from the request query parameters
            full_name = request.query_params.get('full_name')
            created_at = request.query_params.get('created_at')

            # Filter the queryset based on the provided parameters
            queryset = Podcast.objects.all()

            if full_name:
                queryset = queryset.filter(full_name__icontains=full_name)
            
            if created_at:
                queryset = queryset.filter(created_at=created_at)
            
            serializer = PodcastSerializer(queryset, many=True, context={'request': request})

            return Response({'status': True, 'message': 'Data Found Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status' : False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePodcastView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def put(self,request,pk=None) :
        if pk is None:
            return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            podcast = Podcast.objects.get(pk=pk)
            serializer = PodcastSerializer(podcast, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'message': 'Podcast updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Failed to update podcast', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Podcast.DoesNotExist:
            return Response({'status': False, 'message': 'Podcast does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while updating the podcast', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeletePodcastView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def delete(self,request,pk=None) :
        if pk is None:
            return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try :
            podcast = Podcast.objects.get(pk=pk)
            podcast.delete()
            return Response({'status': True, 'message': 'Podcast deleted successfully'}, status=status.HTTP_200_OK)
        except Podcast.DoesNotExist:
            return Response({'status': False, 'message': 'Podcast does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while delete the podcast', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Subscribe API (COMPLETE)
class CreateSubscribeView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    def post(self,request) :
        try :
            email = request.data.get('email').lower()
            if not email:
                return Response({'status': False, 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            else :
                if validate_email(email):
                   # Validate request data using serializer
                    serializer = SubscribeSerializer(data=request.data)
                    if serializer.is_valid():
                        try:
                            user = Subscribe.objects.get(email=email)
                            # If user already exists, return response indicating the user already exists
                            return Response({'status': False, 'message': 'User with this email already subscribe'}, status=status.HTTP_400_BAD_REQUEST)
                        except Subscribe.DoesNotExist:
                            serializer.save(email=email)
                            return Response({'status': True, 'message': 'Subscribe successful'}, status=status.HTTP_200_OK)
                    else:
                        errors = serializer.errors
                        return Response({'status' : False, 'message' : errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'status': False, 'message': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
             return Response({'status':False,'message':f'Error - {e}'},status=status.HTTP_400_BAD_REQUEST)   
        
        
class SubscriberView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    def get(self,request) :
        try :
            # Get parameters from the request query parameters
            email = request.query_params.get('email')
            
            queryset = Subscribe.objects.all()

            if email:
                queryset = queryset.filter(email__icontains=email)
            
            serializer = SubscribeSerializer(queryset, many=True)
            return Response({'status' : True, 'message' : "Data Found Successfully", 'data' : serializer.data},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status' : False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class DeleteSubscribeView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    def delete(self, request, pk=None):
        if pk is None:
            return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Subscribe.objects.get(pk=pk)
            subscription.delete()
            return Response({'status': True, 'message': 'Subscription deleted successfully'}, status=status.HTTP_200_OK)
        except Subscribe.DoesNotExist:
            return Response({'status': False, 'message': 'Subscription does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while deleting the subscription', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# BookRandall API (COMPLETE)
class CreateBookRandallView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def post(self, request) :
        try :
            email = request.data.get('email').lower()
            if not email:
                return Response({'status': False, 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            else :
                if validate_email(email):
                    serializer = BookRandallSerializer(data=request.data)
                    if serializer.is_valid() :
                            # Manually validate each field
                        if not serializer.validated_data.get('first_name'):
                            return Response({'status': False, 'message': 'First name is required'}, status=status.HTTP_400_BAD_REQUEST)
                        if not serializer.validated_data.get('last_name'):
                            return Response({'status': False, 'message': 'Last name is required'}, status=status.HTTP_400_BAD_REQUEST)
                        if not serializer.validated_data.get('subject'):
                            return Response({'status': False, 'message': 'Subject is required'}, status=status.HTTP_400_BAD_REQUEST)
                        if not serializer.validated_data.get('message'):
                            return Response({'status': False, 'message': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
                    
                        # Save the valid data
                        serializer.save(email=email)
                        return Response({'status' : True, 'message' :'BookRandala created successfully' })
                    else :
                        errors = serializer.errors
                        return Response({'status' : False, 'message' : 'Invalid data', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'status': False, 'message': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':False,'message':f'Error - {e}'},status=status.HTTP_400_BAD_REQUEST)   
        
        
class BookRandallView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def get(self,request) :
        try :
            # Get parameters from the request query parameters
            email = request.query_params.get('email')
            created_at = request.query_params.get('created_at')
            
            queryset = BookRandall.objects.all()
            
            if email :
               queryset = queryset.filter(
                Q(first_name__icontains=email) | 
                Q(last_name__icontains=email) | 
                Q(email__icontains=email)
                )
            # Time Formate is Year/Month/Day
            if created_at:
                queryset = queryset.filter(created_at=created_at)
            
            serializer = BookRandallSerializer(queryset, many=True)
            return Response({'status' : True, 'message': 'Data Found Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            
        except Exception as e :
            return Response({'status' : False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteBookRandallView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def delete(self,request,pk=None) :
        if pk is None:
            return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try :
            bookrandall = BookRandall.objects.get(pk=pk)
            bookrandall.delete()
            return Response({'status': True, 'message': 'BookRandall deleted successfully'}, status=status.HTTP_200_OK)
        except BookRandall.DoesNotExist :
            return Response({'status': False, 'message': 'BookRandall does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while deleting the subscription', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


# Videos API's (COMPLETE)
class CreateVideoView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def post(self,request) :
        try :
            serializer = VideoSerializers(data = request.data)
            if serializer.is_valid() :
                if not serializer.validated_data.get('video_file'):
                    return Response({'status': False, 'message': 'Video file is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.validated_data.get('title'):
                    return Response({'status': False, 'message': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.validated_data.get('thumbnails') :
                    return Response({'status': False, 'message': 'Thumbnails is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.validated_data.get('date'):
                    return Response({'status': False, 'message': 'Date is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                # If all validations pass, proceed to save the data
                serializer.save()
                return Response({'status' : True, 'message' : 'Video created successfully'}, status=status.HTTP_201_CREATED)
            else :
                errors = serializer.errors
                return Response({'status' : False, 'message' : 'Invalid data', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
             return Response({'status':False,'message':f'Error - {e}'},status=status.HTTP_400_BAD_REQUEST)   
 
 
class VideosView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def get(self,request) :
        try :
            title = request.query_params.get('title')
            
            # Filter the queryset based on the provided parameters
            queryset = Videos.objects.all()
            
            if title :
                queryset = queryset.filter(title__icontains=title)
            
            serializer = VideoSerializers(queryset,many=True, context={'request': request})
            return Response({'status': True, 'message': 'Data Found Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status' : False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
         
class UpdateVideoView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def put(self,request,pk=None) :
        if pk is None:
            return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            video = Videos.objects.get(pk=pk)
            serializer = VideoSerializers(video, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'message': 'Video updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Failed to update video', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Videos.DoesNotExist:
            return Response({'status': False, 'message': 'Video does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while updating the video', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
        
class DeleteVideoView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def delete(self,request,pk=None) :
        try:
            if pk is None:
                return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
            try :
                video = Videos.objects.get(pk=pk)
                video.delete()
                return Response({'status': True, 'message': 'Video deleted successfully'}, status=status.HTTP_200_OK)
            except Videos.DoesNotExist :
                return Response({'status': False, 'message': 'Video does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while deleting the video', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                
# Testimonial API's (COMPLETE)
class CreateTestimonialView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def post(self,request) :
        try :
            serializer = TestimonialSerializer(data = request.data)
            if serializer.is_valid() :
                if not serializer.validated_data.get('image'):
                    return Response({'status': False, 'message': 'Image file is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not serializer.validated_data.get('name'):
                    return Response({'status': False, 'message': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
                                
                if not serializer.validated_data.get('date'):
                    return Response({'status': False, 'message': 'Date is required'}, status=status.HTTP_400_BAD_REQUEST)
                                
                if not serializer.validated_data.get('content'):
                    return Response({'status': False, 'message': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                # If all validations pass, proceed to save the data
                serializer.save()
                return Response({'status' : True, 'message' : 'Testimonial created successfully'}, status=status.HTTP_201_CREATED)
            else :
                errors = serializer.errors
                return Response({'status' : False, 'message' : 'Invalid data', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
             return Response({'status':False,'message':f'Error - {e}'},status=status.HTTP_400_BAD_REQUEST)   


class TestimonialsView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def get(self,request) :
        try:
            # Get parameters from the request query parameters
            name = request.query_params.get('name')
            date = request.query_params.get('date')

            # Filter the queryset based on the provided parameters
            queryset = Testimonial.objects.all()

            if name:
                queryset = queryset.filter(name__icontains=name)
            
            if date:
                queryset = queryset.filter(date=date)
            
            serializer = TestimonialSerializer(queryset, many=True, context={'request': request})

            return Response({'status': True, 'message': 'Data Found Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status' : False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateTestimonialView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def put(self,request,pk=None) :
        if pk is None:
            return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            testimonial = Testimonial.objects.get(pk=pk)
            serializer = TestimonialSerializer(testimonial, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': True, 'message': 'Testimonial updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Failed to update Testimonial', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Testimonial.DoesNotExist:
            return Response({'status': False, 'message': 'Testimonial does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while updating the Testimonial', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteTestimonialView(APIView) :
    authentication_classes = [CustomJWTAuthentication]
    def delete(self,request,pk=None) :
        if pk is None:
                return Response({'status': False, 'message': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try :
            testimonial = Testimonial.objects.get(pk=pk)
            testimonial.delete()
            return Response({'status': True, 'message': 'Testimonial deleted successfully'}, status=status.HTTP_200_OK)
        except Testimonial.DoesNotExist :
            return Response({'status': False, 'message': 'Testimonial does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': False, 'message': 'An error occurred while deleting the testimonial', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        