# views.py
from datetime import timedelta
from urllib import request
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlbumsPrices, Chat, CustomUser, Message, Photographer, Spot, SessionAlbum, Img, SpotLike, Follower, Order, Wave
from .serializers import  AlbumsPricesSerializer, ChatSerializer, CustomUserSerializer, MessageSerializer, MyTokenObtainPairSerializer, PhotographerSerializer, SessionAlbumByPhotographerSerializer, SessionAlbumBySpotSerializer, SessionAlbumWithDetailsSerializer, SpotSerializer, SessionAlbumSerializer, ImgSerializer, SpotLikeSerializer, FollowerSerializer, OrderSerializer, WaveSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



    
class PhotographerListCreateView(generics.ListCreateAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer

    def perform_create(self, serializer):
        # Call the parent perform_create to save the photographer instance
        photographer = serializer.save()
        # Access the user associated with the photographer
        user = photographer.user
        # Update is_photographer to True
        user.is_photographer = True
        user.save()


class PhotographerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photographer.objects.all()  # Add this line
    serializer_class = PhotographerSerializer

    def get(self, request, *args, **kwargs):
        photographer = self.get_object()
        photographer_name = photographer.user.get_full_name()
        followers_count = Follower.objects.filter(photographer=photographer).count()
        serializer = self.get_serializer(photographer)
        data = serializer.data
        data['photographer_name'] = photographer_name
        data['followers_count'] = followers_count

        return Response(data, status=status.HTTP_200_OK)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class PhotographerByUserIdView(generics.RetrieveAPIView):
    serializer_class = PhotographerSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        photographer = get_object_or_404(Photographer, user__id=user_id)
        photographer_name = photographer.user.get_full_name()
        followers_count = Follower.objects.filter(photographer=photographer).count()
        serializer = self.get_serializer(photographer)
        data = serializer.data
        data['photographer_name'] = photographer_name
        data['followers_count'] = followers_count

        return Response(data, status=status.HTTP_200_OK)



class SpotListCreateView(generics.ListCreateAPIView):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer

class SpotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer




class SessionAlbumListCreateView(generics.ListCreateAPIView):
    queryset = SessionAlbum.objects.all()
    serializer_class = SessionAlbumSerializer

class SessionAlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SessionAlbum.objects.all()
    serializer_class = SessionAlbumSerializer





# class PersonalAlbumListCreateView(generics.ListCreateAPIView):
#     queryset = PersonalAlbum.objects.all()
#     serializer_class = PersonalAlbumSerializer

# class PersonalAlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PersonalAlbum.objects.all()
#     serializer_class = PersonalAlbumSerializer





class ImgListCreateView(generics.ListCreateAPIView):
    queryset = Img.objects.all()
    serializer_class = ImgSerializer

class ImgDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Img.objects.all()
    serializer_class = ImgSerializer



# class ImgListCreateBulkView(generics.ListCreateAPIView):
#     queryset = Img.objects.all()
#     serializer_class = ImgSerializer

#     def create(self, request, *args, **kwargs):
#         session_album_id = request.data.get('session_album_id')
#         images_arrays = request.data.get('images_arrays', [])

#         if not session_album_id or not images_arrays:
#             return Response({'error': 'session_album_id and images_arrays are required.'}, status=400)

#         # Bulk create PersonalAlbum instances
#         personal_albums = [PersonalAlbum(session_album_id=session_album_id) for _ in images_arrays]
#         PersonalAlbum.objects.bulk_create(personal_albums)

#         # Bulk create Img instances
#         img_instances = []
#         for personal_album, img_array in zip(personal_albums, images_arrays):
#             # Set the cover image for the first PersonalAlbum in each iteration+
#             if img_array:
#                 personal_album.cover_image = img_array[0]
#                 personal_album.save()

#             for image_url in img_array:
#                 img_instance = Img(photo=image_url, personal_album=personal_album)
#                 img_instances.append(img_instance)

#         Img.objects.bulk_create(img_instances)

#         # update_prices_view(request, session_album_id)

#         return Response({'success': 'Almost there! All the albums created successfully, now we update the prices.'}, status=201)








class SpotLikeListCreateView(generics.ListCreateAPIView):
    queryset = SpotLike.objects.all()
    serializer_class = SpotLikeSerializer


class SpotLikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpotLike.objects.all()
    serializer_class = SpotLikeSerializer


class SpotLikesByUserListView(generics.ListAPIView):
    serializer_class = SpotLikeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return SpotLike.objects.filter(user__id=user_id)

class SpotLikesBySpotListView(generics.ListAPIView):
    serializer_class = SpotLikeSerializer

    def get_queryset(self):
        spot_id = self.kwargs['spot_id']
        return SpotLike.objects.filter(spot__id=spot_id)





class FollowerListCreateView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

class FollowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer


class FollowersByUserListView(generics.ListAPIView):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follower.objects.filter(user__id=user_id)

class FollowersByPhotographerListView(generics.ListAPIView):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        photographer_id = self.kwargs['photographer_id']
        return Follower.objects.filter(photographer__id=photographer_id)





class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




# class CreateAlbumView(APIView):
#     def post(self, request, *args, **kwargs):
#         """
#         Handle POST request to create a Session Album, Personal Album, and Images.
#         """
#         session_album_data = request.data.get('session_album', {})
#         personal_albums_data = request.data.get('personal_albums', [])
#         images_data = request.data.get('images', [])

#         session_album_serializer = SessionAlbumSerializer(data=session_album_data)
#         if session_album_serializer.is_valid():
#             session_album = session_album_serializer.save()
#         else:
#             return Response(session_album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         personal_albums = []
#         for personal_album_data in personal_albums_data:
#             personal_album_data['session_album'] = session_album.id
#             personal_album_serializer = PersonalAlbumSerializer(data=personal_album_data)
#             if personal_album_serializer.is_valid():
#                 personal_album = personal_album_serializer.save()
#                 personal_albums.append(personal_album)
#             else:
#                 session_album.delete()
#                 return Response(personal_album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         for personal_album in personal_albums:
#             for image_data in images_data:
#                 image_data['personal_album'] = personal_album.id
#                 image_serializer = ImgSerializer(data=image_data)
#                 if image_serializer.is_valid():
#                     image_serializer.save()
#                 else:
#                     session_album.delete()
#                     for album in personal_albums:
#                         album.delete()
#                     return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"detail": "Album created successfully."}, status=status.HTTP_201_CREATED)
    


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer












# class ImgByPersonalAlbumListView(generics.ListAPIView):
#     serializer_class = ImgByPersonalAlbumSerializer

#     def get_queryset(self):
#         personal_album_id = self.kwargs['personal_album_id']
#         return Img.objects.filter(personal_album__id=personal_album_id)
    


    



class SessionAlbumListAPIView(generics.ListAPIView):
    queryset = SessionAlbum.objects.all()
    serializer_class = SessionAlbumWithDetailsSerializer



class SessionAlbumByPhotographer(generics.ListAPIView):
    serializer_class = SessionAlbumByPhotographerSerializer

    def get_queryset(self):
        photographer_id = self.kwargs['photographer_id']  # Assuming the photographer_id is passed as a URL parameter
        queryset = SessionAlbum.objects.filter(photographer__id=photographer_id)
        return queryset


class SessionAlbumBySpot(generics.ListAPIView):
    serializer_class = SessionAlbumBySpotSerializer

    def get_queryset(self):
        spot_id = self.kwargs['spot_id']  # Assuming the spot_id is passed as a URL parameter
        queryset = SessionAlbum.objects.filter(spot__id=spot_id)
        return queryset


# class PersonalAlbumListView(generics.ListAPIView):
#     serializer_class = PersonalAlbumSerializer

#     def get_queryset(self):
#         session_album_id = self.kwargs['session_album_id']
#         personal_albums = PersonalAlbum.objects.filter(session_album_id=session_album_id)
#         return personal_albums

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         # Add image count to serializer context
#         session_album_id = self.kwargs['session_album_id']
#         context['image_counts'] = {album.id: album.img_set.count() for album in self.get_queryset()}
#         return context






from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import SessionAlbum, Img









class AlbumsPricesListCreateView(generics.ListCreateAPIView):
    queryset = AlbumsPrices.objects.all()
    serializer_class = AlbumsPricesSerializer

class AlbumsPricesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlbumsPrices.objects.all()
    serializer_class = AlbumsPricesSerializer






# @method_decorator(csrf_exempt, name='dispatch')
# class UpdatePricesView(APIView):
#     def post(self, request, session_album_id):
#         session_album = get_object_or_404(SessionAlbum, id=session_album_id)

#         # Find the relevant AlbumsPrices instance for the session_album
#         albums_prices, created = AlbumsPrices.objects.get_or_create(session_album=session_album)

#         # Update prices for PersonalAlbums
#         personal_albums = PersonalAlbum.objects.filter(session_album=session_album)

#         for personal_album in personal_albums:
#             image_count = personal_album.get_image_count()

#             # Update price based on image count
#             if 1 <= image_count <= 5:
#                 personal_album.price = albums_prices.price_1_to_5
#             elif 6 <= image_count <= 10:
#                 personal_album.price = albums_prices.price_6_to_10
#             elif 11 <= image_count <= 20:
#                 personal_album.price = albums_prices.price_11_to_20
#             elif 21 <= image_count <= 50:
#                 personal_album.price = albums_prices.price_21_to_50
#             elif image_count >= 51:
#                 personal_album.price = albums_prices.price_51_plus

#             personal_album.save()

#         # Update prices for Images
#         Img.objects.filter(personal_album__session_album=session_album).update(
#             price=albums_prices.singlePhotoPrice
#         )

#         # Return an empty response with HTTP 204 No Content status
#         return HttpResponse(status=204)
    




# ************************************************        S3           ****************************************
import boto3
import uuid
from django.http import JsonResponse
from rest_framework.decorators import api_view



from django.conf import settings


@api_view(['GET'])
def get_batch_presigned_urlssss(request):
    s3 = boto3.client('s3', region_name='us-east-2', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    

    # Number of presigned URLs to generate (assuming each URL corresponds to an image)
    num_urls = int(request.GET.get('num_urls', 1))  # Default to 1 if not specified
    
    # Generate presigned URLs for batch upload
    presigned_urls = []
    for _ in range(num_urls):
        unique_filename = f'{uuid.uuid4()}.jpg'
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram', 'Key': unique_filename },  # Customize Key as needed
            ExpiresIn=3600  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)
    
    return JsonResponse({'urls': presigned_urls})








import requests
from datetime import datetime
from PIL import Image
from io import BytesIO
from functools import lru_cache

@api_view(['POST'])
def create_images_and_waves(request):
    original_urls = request.data.get('original_urls', [])
    watermarked_urls = request.data.get('watermarked_urls', [])
    session_album_id = request.data.get('session_album')

    if len(original_urls) != len(watermarked_urls):
        return Response({'error': 'Mismatched number of original and watermarked URLs'}, status=status.HTTP_400_BAD_REQUEST)

    images_and_waves = []
    current_wave = None
    previous_datetime = None

    TIME_GAP_THRESHOLD = 5  # seconds

    for original_url, watermarked_url in zip(original_urls, watermarked_urls):
        datetime_original = get_datetime_original_from_image(original_url)
        print(datetime_original)

        if datetime_original:
            if not current_wave or (datetime_original - previous_datetime) > timedelta(seconds=TIME_GAP_THRESHOLD):
                current_wave = create_wave(session_album_id, original_url)
                previous_datetime = datetime_original

            images_and_waves.append((original_url, watermarked_url, current_wave))
        else:
            print(f"Skipping image {original_url} due to missing DateTimeOriginal.")

    create_images(images_and_waves)

    return Response({'message': 'Images and Waves created successfully'}, status=status.HTTP_201_CREATED)

def create_wave(session_album_id, cover_image_url):
    wave = Wave.objects.create(session_album_id=session_album_id, cover_image=cover_image_url)
    return wave

def create_images(images_and_waves):
    images_to_create = [
        Img(photo=original_url, WatermarkedPhoto=watermarked_url, wave=wave)
        for original_url, watermarked_url, wave in images_and_waves
    ]
    Img.objects.bulk_create(images_to_create)

@lru_cache(maxsize=128)  # Cache up to 128 URLs
def get_datetime_original_from_image(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        exif_data = image._getexif()
        datetime_original = exif_data.get(36867) if exif_data else None
        return datetime.strptime(datetime_original, '%Y:%m:%d %H:%M:%S') if datetime_original else None
    except Exception as e:
        print(f"Error getting DateTimeOriginal from image: {e}")
        return None

    # def create_personal_album(session_album_id, cover_image):
#     # Create a new personal album associated with the session album
#     personal_album = PersonalAlbum.objects.create(session_album_id=session_album_id, cover_image=cover_image)
#     return personal_album
    
@api_view(['GET'])
def get_waves_for_session_album(request, session_album_id):
    try:
        waves = Wave.objects.filter(session_album=session_album_id)
        serializer = WaveSerializer(waves, many=True)
        return Response(serializer.data)
    except Wave.DoesNotExist:
        return Response({'message': 'No waves found for the provided SessionAlbum ID.'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
def get_images_for_wave(request, wave_id):
    try:
        images = Img.objects.filter(wave=wave_id)
        serializer = ImgSerializer(images, many=True)
        return Response(serializer.data)
    except Img.DoesNotExist:
        return Response({'message': 'No images found for the provided Wave ID.'}, status=status.HTTP_404_NOT_FOUND)





@api_view(['POST'])
def get_images_for_multiple_waves(request):
    try:
        wave_ids = request.data.get('waveIds', [])
        if not wave_ids:
            return Response({'message': 'No wave IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        images = Img.objects.filter(wave__in=wave_ids)
        serializer = ImgSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_watermarked_photos_by_wave(request, wave_id):
    try:
        images = Img.objects.filter(wave=wave_id).values('WatermarkedPhoto')
        return Response(list(images), status=status.HTTP_200_OK)
    except Img.DoesNotExist:
        return Response({'message': 'No images found for the provided Wave ID.'}, status=status.HTTP_404_NOT_FOUND)
    



