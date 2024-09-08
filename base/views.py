# views.py
from datetime import timedelta
from urllib import request
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response

from base.pagination import CustomPageNumberPagination
from .models import AlbumsPrices, AlbumsPricesForVideos, Chat, CustomUser, Message, Photographer, Purchase, PurchaseItem, Spot, SessionAlbum, Img, SpotLike, Follower, Video, Wave
from .serializers import  AlbumsPricesForVideosSerializer, AlbumsPricesSerializer, ChatSerializer, CustomUserSerializer, MessageSerializer, MyTokenObtainPairSerializer, PhotographerSerializer, PurchaseItemSerializer, PurchaseSerializer, SessionAlbumByPhotographerSerializer, SessionAlbumBySpotSerializer, SessionAlbumWithDetailsSerializer, SpotSerializer, SessionAlbumSerializer, ImgSerializer, SpotLikeSerializer, FollowerSerializer, VideoSerializer, WaveSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
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


class PhotographerDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer

    def perform_update(self, serializer):
        photographer = serializer.save()

        

class PhotographerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer

    def get(self, request, *args, **kwargs):
        photographer = self.get_object()

        # Get the photographer's full name and follower count
        photographer_name = photographer.user.get_full_name()
        followers_count = Follower.objects.filter(photographer=photographer).count()

        # Get the count of SessionAlbums associated with the photographer
        session_album_count = SessionAlbum.objects.filter(photographer=photographer).count()

        # Get the count of unique Spots associated with the photographer's SessionAlbums
        unique_spots_count = SessionAlbum.objects.filter(photographer=photographer).values('spot').distinct().count()

        # Serialize the photographer data
        serializer = self.get_serializer(photographer)
        data = serializer.data

        # Add additional data to the response
        data['photographer_name'] = photographer_name
        data['followers_count'] = followers_count
        data['session_album_count'] = session_album_count
        data['unique_spots_count'] = unique_spots_count

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

        # Get the photographer's full name and follower count
        photographer_name = photographer.user.get_full_name()
        followers_count = Follower.objects.filter(photographer=photographer).count()

        # Get the count of SessionAlbums associated with the photographer
        session_album_count = SessionAlbum.objects.filter(photographer=photographer).count()

        # Get the count of unique Spots associated with the photographer's SessionAlbums
        unique_spots_count = SessionAlbum.objects.filter(photographer=photographer).values('spot').distinct().count()

        # Serialize the photographer data
        serializer = self.get_serializer(photographer)
        data = serializer.data

        # Add additional data to the response
        data['photographer_name'] = photographer_name
        data['followers_count'] = followers_count
        data['session_album_count'] = session_album_count
        data['unique_spots_count'] = unique_spots_count

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



# *************************************************************************************************************************************

class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class PurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer



class PurchaseItemListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer

class PurchaseItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer


class CreatePurchaseWithImagesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract purchase data
            purchase_data = {
                "photographer": request.data.get('photographer_id'),
                "photographer_name": request.data.get('photographer_name'),
                "sessDate": request.data.get('sessDate'),
                "SessionAlbum": request.data.get('session_album_id'),
                "spot_name": request.data.get('spot_name'),
                "surfer": request.data.get('surfer_id'),
                "surfer_name": request.data.get('surfer_name'),
                "total_item_quantity": request.data.get('total_item_quantity'),
                "total_price": request.data.get('total_price'),
            }
            purchase_serializer = PurchaseSerializer(data=purchase_data)
            
            # Validate and save Purchase
            if purchase_serializer.is_valid():
                purchase = purchase_serializer.save()

                # Extract image IDs
                image_ids = request.data.get('image_ids', [])
                for img_id in image_ids:
                    img = Img.objects.get(id=img_id)
                    purchase_item_data = {
                        "PurchaseId": purchase.id,
                        "Img": img.id
                    }
                    purchase_item_serializer = PurchaseItemSerializer(data=purchase_item_data)
                    if purchase_item_serializer.is_valid():
                        purchase_item_serializer.save()
                    else:
                        return Response(purchase_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(purchase_serializer.data, status=status.HTTP_201_CREATED)
            return Response(purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Img.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)


class CreatePurchaseWithVideosView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract purchase data
            purchase_data = {
                "photographer": request.data.get('photographer_id'),
                "photographer_name": request.data.get('photographer_name'),
                "sessDate": request.data.get('sessDate'),
                "SessionAlbum": request.data.get('session_album_id'),
                "spot_name": request.data.get('spot_name'),
                "surfer": request.data.get('surfer_id'),
                "surfer_name": request.data.get('surfer_name'),
                "total_item_quantity": request.data.get('total_item_quantity'),
                "total_price": request.data.get('total_price'),
            }
            purchase_serializer = PurchaseSerializer(data=purchase_data)
            
            # Validate and save Purchase
            if purchase_serializer.is_valid():
                purchase = purchase_serializer.save()

                # Extract video IDs
                video_ids = request.data.get('video_ids', [])
                for video_id in video_ids:
                    video = Video.objects.get(id=video_id)
                    purchase_item_data = {
                        "PurchaseId": purchase.id,
                        "Video": video.id
                    }
                    purchase_item_serializer = PurchaseItemSerializer(data=purchase_item_data)
                    if purchase_item_serializer.is_valid():
                        purchase_item_serializer.save()
                    else:
                        return Response(purchase_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(purchase_serializer.data, status=status.HTTP_201_CREATED)
            return Response(purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)



class CreatePurchaseWithWavesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract purchase data with additional fields
            purchase_data = {
                "photographer": request.data.get('photographer_id'),
                "photographer_name": request.data.get('photographer_name'),
                "sessDate": request.data.get('sessDate'),
                "SessionAlbum": request.data.get('session_album_id'),
                "spot_name": request.data.get('spot_name'),
                "surfer": request.data.get('surfer_id'),
                "surfer_name": request.data.get('surfer_name'),
                "total_price": request.data.get('total_price'),
            }
            purchase_serializer = PurchaseSerializer(data=purchase_data)
            
            # Validate and save Purchase
            if purchase_serializer.is_valid():
                purchase = purchase_serializer.save()

                # Extract wave IDs and initialize total_item_quantity
                wave_ids = request.data.get('wave_ids', [])
                total_item_quantity = 0
                
                for wave_id in wave_ids:
                    wave = Wave.objects.get(id=wave_id)
                    images = wave.img_set.all()  # Get all images associated with the wave

                    for img in images:
                        purchase_item_data = {
                            "PurchaseId": purchase.id,
                            "Img": img.id
                        }
                        purchase_item_serializer = PurchaseItemSerializer(data=purchase_item_data)
                        if purchase_item_serializer.is_valid():
                            purchase_item_serializer.save()
                            total_item_quantity += 1
                        else:
                            return Response(purchase_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                # Update total_item_quantity in the purchase
                purchase.total_item_quantity = total_item_quantity
                purchase.save()

                return Response(purchase_serializer.data, status=status.HTTP_201_CREATED)
            return Response(purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Wave.DoesNotExist:
            return Response({"error": "Wave not found"}, status=status.HTTP_404_NOT_FOUND)
        except Img.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        




# class GetPurchasedItemsBySurfer(APIView):
#     def get(self, request, surfer_id):
#         try:
#             # Find all Purchases for the given surfer
#             purchases = Purchase.objects.filter(surfer_id=surfer_id)
#             items_by_purchase = {}

#             for purchase in purchases:
#                 purchase_items = PurchaseItem.objects.filter(PurchaseId=purchase.id)
#                 items_by_purchase[purchase.id] = []

#                 for item in purchase_items:
#                     # If the item is an image, add it to the list
#                     if item.Img:
#                         items_by_purchase[purchase.id].append({
#                             'type': 'image',
#                             'id': item.Img.id,
#                             'photo': item.Img.photo,
#                             'WatermarkedPhoto': item.Img.WatermarkedPhoto,
#                             # Add other fields as necessary
#                         })

#                     # If the item is a video, add it to the list
#                     if item.Video:
#                         items_by_purchase[purchase.id].append({
#                             'type': 'video',
#                             'id': item.Video.id,
#                             'video': item.Video.video,
#                             'WatermarkedVideo': item.Video.WatermarkedVideo,
#                             # Add other fields as necessary
#                         })

#             return Response({'items_by_purchase': items_by_purchase}, status=status.HTTP_200_OK)

#         except Purchase.DoesNotExist:
#             return Response({"error": "No purchases found for this user"}, status=status.HTTP_404_NOT_FOUND)
        


class GetPurchasedItemsBySurfer(APIView):
    def get(self, request, surfer_id):
        try:
            # Find all Purchases for the given surfer
            purchases = Purchase.objects.filter(surfer_id=surfer_id)
            purchased_images = {}
            purchased_videos = {}

            for purchase in purchases:
                purchase_items = PurchaseItem.objects.filter(PurchaseId=purchase.id)

                # Gather images
                for item in purchase_items:
                    if item.Img:
                        if purchase.id not in purchased_images:
                            purchased_images[purchase.id] = []
                        purchased_images[purchase.id].append({
                            'id': item.Img.id,
                            'photo': item.Img.photo,
                            'WatermarkedPhoto': item.Img.WatermarkedPhoto,
                            # Add other fields as necessary
                        })
                    
                    # Gather videos
                    if item.Video:
                        if purchase.id not in purchased_videos:
                            purchased_videos[purchase.id] = []
                        purchased_videos[purchase.id].append({
                            'id': item.Video.id,
                            'video': item.Video.video,
                            'WatermarkedVideo': item.Video.WatermarkedVideo,
                            # Add other fields as necessary
                        })

            return Response({
                'purchased_images': purchased_images,
                'purchased_videos': purchased_videos
            }, status=status.HTTP_200_OK)

        except Purchase.DoesNotExist:
            return Response({"error": "No purchases found for this user"}, status=status.HTTP_404_NOT_FOUND)
        




class GetPurchasesByPhotographerName(APIView):
    def get(self, request, photographer_name):
        try:
            # Filter purchases by photographer_name
            purchases = Purchase.objects.filter(photographer_name=photographer_name)

            if not purchases.exists():
                return Response({"error": "No purchases found for this photographer"}, status=status.HTTP_404_NOT_FOUND)

            purchase_list = []

            for purchase in purchases:
                # Format dates
                formatted_order_date = purchase.order_date.strftime('%Y-%m-%d') if purchase.order_date else ''
                formatted_sess_date = purchase.sessDate.strftime('%Y-%m-%d') if purchase.sessDate else ''
                
                purchase_data = {
                    'id': purchase.id,
                    'photographer_id': purchase.photographer.id,
                    'surfer_id': purchase.surfer.id,
                    'order_date': formatted_order_date,
                    'total_price': purchase.total_price,
                    'total_item_quantity': purchase.total_item_quantity,
                    'session_album_id': purchase.SessionAlbum.id if purchase.SessionAlbum else None,
                    'spot_name': purchase.spot_name,
                    'photographer_name': purchase.photographer_name,
                    'surfer_name': purchase.surfer_name,
                    'sessDate': formatted_sess_date,
                }
                purchase_list.append(purchase_data)

            return Response(purchase_list, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class PurchasesByPhotographerView(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        photographer_id = self.kwargs['photographer_id']
        return Purchase.objects.filter(photographer_id=photographer_id)

class PurchasesBySurferView(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        surfer_id = self.kwargs['surfer_id']
        return Purchase.objects.filter(surfer_id=surfer_id)
    


 # *************************************************************************************************************************************

    


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
    pagination_class = CustomPageNumberPagination



class SessionAlbumDetailByIDAPIView(generics.RetrieveAPIView):
    queryset = SessionAlbum.objects.all()
    serializer_class = SessionAlbumWithDetailsSerializer
    lookup_field = 'id'



class SessionAlbumByPhotographer(generics.ListAPIView):
    serializer_class = SessionAlbumByPhotographerSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        photographer_id = self.kwargs['photographer_id']  # Assuming the photographer_id is passed as a URL parameter
        queryset = SessionAlbum.objects.filter(photographer__id=photographer_id)
        return queryset


class SessionAlbumBySpot(generics.ListAPIView):
    serializer_class = SessionAlbumBySpotSerializer
    pagination_class = CustomPageNumberPagination

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




class AlbumsPricesForVideosListCreateView(generics.ListCreateAPIView):
    queryset = AlbumsPricesForVideos.objects.all()
    serializer_class = AlbumsPricesForVideosSerializer

class AlbumsPricesForVideosDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlbumsPricesForVideos.objects.all()
    serializer_class = AlbumsPricesForVideosSerializer





class AlbumsPricesBySess(generics.GenericAPIView):
    serializer_class = AlbumsPricesSerializer

    def get(self, request, session_album_id):
        try:
            albums_prices = AlbumsPrices.objects.get(session_album_id=session_album_id)
            serializer = self.get_serializer(albums_prices)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AlbumsPrices.DoesNotExist:
            return Response({"error": "AlbumsPrices not found"}, status=status.HTTP_404_NOT_FOUND)



class AlbumsPricesForVideosBySess(generics.GenericAPIView):
    serializer_class = AlbumsPricesForVideosSerializer

    def get(self, request, session_album_id):
        try:
            albums_prices = AlbumsPricesForVideos.objects.get(session_album_id=session_album_id)
            serializer = self.get_serializer(albums_prices)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AlbumsPricesForVideos.DoesNotExist:
            return Response({"error": "AlbumsPrices not found"}, status=status.HTTP_404_NOT_FOUND)




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
from botocore.config import Config


@api_view(['GET'])
def get_batch_presigned_urlssss(request):
    # Configure S3 client with Transfer Acceleration
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'use_accelerate_endpoint': True})
    )

    # Number of presigned URLs to generate (assuming each URL corresponds to an image)
    num_urls = int(request.GET.get('num_urls', 1))  # Default to 1 if not specified
    
    # Generate presigned URLs for batch upload
    presigned_urls = []
    for _ in range(num_urls):
        unique_filename = f'{uuid.uuid4()}.jpg'
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram', 'Key': unique_filename},  # Customize Key as needed
            ExpiresIn=360000  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)
    
    return JsonResponse({'urls': presigned_urls})



@api_view(['GET'])
def presigned_urls_for_originals(request):
    # Configure S3 client with Transfer Acceleration
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'use_accelerate_endpoint': True})
    )

    # Number of presigned URLs to generate (assuming each URL corresponds to an image)
    num_urls = int(request.GET.get('num_urls', 1))  # Default to 1 if not specified
    
    # Generate presigned URLs for batch upload
    presigned_urls = []
    for _ in range(num_urls):
        unique_filename = f'{uuid.uuid4()}.jpg'
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram', 'Key': unique_filename},  # Customize Key as needed
            ExpiresIn=360000  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)
    
    return JsonResponse({'urls': presigned_urls})



@api_view(['GET'])
def presigned_urls_for_watermarked(request):
    # Configure S3 client with Transfer Acceleration
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'use_accelerate_endpoint': True})
    )

    # Number of presigned URLs to generate (assuming each URL corresponds to an image)
    num_urls = int(request.GET.get('num_urls', 1))  # Default to 1 if not specified
    
    # Generate presigned URLs for batch upload
    presigned_urls = []
    for _ in range(num_urls):
        unique_filename = f'{uuid.uuid4()}.jpg'
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram-watermarked', 'Key': unique_filename},  # Customize Key as needed
            ExpiresIn=360000  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)
    
    return JsonResponse({'urls': presigned_urls})




@api_view(['GET'])
def presigned_urls_for_original_videos(request):
    # Configure S3 client with Transfer Acceleration
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'use_accelerate_endpoint': True})
    )

    # Number of presigned URLs to generate (assuming each URL corresponds to an image)
    num_urls = int(request.GET.get('num_urls', 1))  # Default to 1 if not specified
    
    # Generate presigned URLs for batch upload
    presigned_urls = []
    for _ in range(num_urls):
        unique_filename = f'{uuid.uuid4()}.mp4'
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram-original-video', 'Key': unique_filename},  # Customize Key as needed
            ExpiresIn=360000  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)
    
    return JsonResponse({'urls': presigned_urls})



@api_view(['GET'])
def presigned_urls_for_watermarked_videos(request):
    # Configure S3 client with Transfer Acceleration
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'use_accelerate_endpoint': True})
    )

    # Number of presigned URLs to generate (assuming each URL corresponds to an image)
    num_urls = int(request.GET.get('num_urls', 1))  # Default to 1 if not specified
    
    # Generate presigned URLs for batch upload
    presigned_urls = []
    for _ in range(num_urls):
        unique_filename = f'{uuid.uuid4()}.mp4'
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram-transformed-video', 'Key': unique_filename},  # Customize Key as needed
            ExpiresIn=360000  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)
    
    return JsonResponse({'urls': presigned_urls})






@api_view(['GET'])
def presigned_urls_for_profile_pictures(request):
    # Configure S3 client with Transfer Acceleration
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'use_accelerate_endpoint': True})
    )

    # Number of presigned URLs to generate (assuming each URL corresponds to an image)
    num_urls = int(request.GET.get('num_urls', 1))  # Default to 1 if not specified
    
    # Generate presigned URLs for batch upload
    presigned_urls = []
    for _ in range(num_urls):
        unique_filename = f'{uuid.uuid4()}.jpg'
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram-profile-images', 'Key': unique_filename},  # Customize Key as needed
            ExpiresIn=360000  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)
    
    return JsonResponse({'urls': presigned_urls})


import requests
from datetime import datetime
from PIL import Image
from io import BytesIO
from functools import lru_cache




@api_view(['POST'])
def create_videos(request):
    video_urls = request.data.get('video', [])
    watermarked_video_urls = request.data.get('WatermarkedVideo', [])
    img_urls = request.data.get('img', [])
    session_album_id = request.data.get('SessionAlbum')

    # Validate SessionAlbum ID
    if not session_album_id:
        return Response({"error": "SessionAlbum ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate that the number of URLs match
    if len(video_urls) != len(watermarked_video_urls) or len(video_urls) != len(img_urls):
        return Response({"error": "The number of videos, watermarked videos, and images must be the same"}, status=status.HTTP_400_BAD_REQUEST)

    # Try to retrieve the SessionAlbum
    try:
        session_album = SessionAlbum.objects.get(id=session_album_id)
    except SessionAlbum.DoesNotExist:
        return Response({"error": "SessionAlbum not found"}, status=status.HTTP_404_NOT_FOUND)

    # Save the data in a new way, for example, by creating individual video entries
    created_videos = []
    for video_url, watermarked_video_url, img_url in zip(video_urls, watermarked_video_urls, img_urls):
        try:
            video = Video.objects.create(
                video=video_url,
                WatermarkedVideo=watermarked_video_url,
                img=img_url,
                SessionAlbum=session_album
            )
            created_videos.append(video)
        except Exception as e:
            # Return an error if something goes wrong
            return Response({"error": "An error occurred while saving the videos"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Return the created video details
    return Response({
        "message": "Videos created successfully",
        "created_videos": [video.id for video in created_videos]
    }, status=status.HTTP_201_CREATED)

    
from django.utils.dateparse import parse_datetime

from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Img, Wave, SessionAlbum

@api_view(['POST'])
def create_images_and_waves(request):
    original_urls = request.data.get('original_urls', [])
    watermarked_urls = request.data.get('watermarked_urls', [])
    session_album_id = request.data.get('session_album')
    exif_dates = request.data.get('exif_dates', [])

    # Validate that URL lists are the same length
    if len(original_urls) != len(watermarked_urls):
        return Response({'error': 'Mismatched number of URLs'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if all EXIF dates are "null"
    if all(exif_date == "null" for exif_date in exif_dates):
        # If all EXIF dates are "null", create images with wave = null
        images_to_create = [
            Img(photo=original_url, WatermarkedPhoto=watermarked_url, SessionAlbum_id=session_album_id)
            for original_url, watermarked_url in zip(original_urls, watermarked_urls)
        ]
        Img.objects.bulk_create(images_to_create)
        
        # Mark the SessionAlbum as active but not divided into waves
        session_album = SessionAlbum.objects.get(id=session_album_id)
        session_album.dividedToWaves = False
        session_album.active = True
        session_album.save()

        return Response({'message': 'Images created successfully without waves'}, status=status.HTTP_201_CREATED)

    images_and_waves = []
    current_wave = None
    previous_datetime = None
    TIME_GAP_THRESHOLD = 5  # seconds

    # Lists to keep track of images without EXIF data
    no_exif_images = []

    try:
        for i, (original_url, watermarked_url) in enumerate(zip(original_urls, watermarked_urls)):
            exif_date = exif_dates[i] if i < len(exif_dates) else None

            if exif_date != "null":
                try:
                    # Convert EXIF date string to datetime object
                    datetime_original = datetime.strptime(exif_date, "%Y:%m:%d %H:%M:%S")
                except ValueError:
                    datetime_original = None

                if datetime_original:
                    # Handle images with EXIF data
                    if not current_wave or (datetime_original - previous_datetime) > timedelta(seconds=TIME_GAP_THRESHOLD):
                        current_wave = create_wave(session_album_id, watermarked_url)
                        previous_datetime = datetime_original

                    images_and_waves.append((original_url, watermarked_url, current_wave))
                else:
                    # If datetime conversion fails, treat it as no EXIF data
                    no_exif_images.append((original_url, watermarked_url))
            else:
                # Handle images without EXIF data
                no_exif_images.append((original_url, watermarked_url))

        # Process images with EXIF data
        if images_and_waves:
            create_images(images_and_waves)
        
        # Process images without EXIF data
        if no_exif_images:
            for original_url, watermarked_url in no_exif_images:
                wave = create_wave(session_album_id, watermarked_url)
                create_images([(original_url, watermarked_url, wave)])
        
        # Mark the SessionAlbum as active and dividedToWaves as True after successful processing
        session_album = SessionAlbum.objects.get(id=session_album_id)
        session_album.dividedToWaves = True
        session_album.active = True
        session_album.save()

        return Response({'message': 'Images and Waves created successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Error creating waves: {e}")

        # Create images without waves in case of an error
        images_to_create = [
            Img(photo=original_url, WatermarkedPhoto=watermarked_url, SessionAlbum_id=session_album_id)
            for original_url, watermarked_url in zip(original_urls, watermarked_urls)
        ]
        Img.objects.bulk_create(images_to_create)

        # Update the session album to set dividedToWaves to False if an error occurred
        try:
            session_album = SessionAlbum.objects.get(id=session_album_id)
            session_album.dividedToWaves = False  # Set to False if any error occurs
            session_album.save()
        except SessionAlbum.DoesNotExist:
            print(f"SessionAlbum with id {session_album_id} does not exist.")

        return Response({'message': 'Images created successfully, but wave creation failed'}, status=status.HTTP_201_CREATED)

def create_wave(session_album_id, cover_image_url):
    wave = Wave.objects.create(session_album_id=session_album_id, cover_image=cover_image_url)
    return wave

def create_images(images_and_waves):
    images_to_create = [
        Img(photo=original_url, WatermarkedPhoto=watermarked_url, wave=wave, SessionAlbum_id=wave.session_album_id if wave else None)
        for original_url, watermarked_url, wave in images_and_waves
    ]
    Img.objects.bulk_create(images_to_create)



@lru_cache(maxsize=1000000)
def get_datetime_original_from_image(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        exif_data = image._getexif()
        
        if not exif_data:
            return None

        # Possible EXIF tags for dates
        date_tags = [36867, 36868, 306]  # DateTimeOriginal, DateTimeDigitized, DateTime

        datetime_original = None
        for tag in date_tags:
            datetime_str = exif_data.get(tag)
            if datetime_str:
                try:
                    datetime_original = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
                    break
                except ValueError as ve:
                    print(f"Error parsing date string: {datetime_str} for tag {tag}, error: {ve}")
        
        return datetime_original
    except Exception as e:
        print(f"Error getting DateTimeOriginal from image: {e}")
        return None

    


class GetImagesBySessionAlbumView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request, session_album_id):
        try:
            session_album = SessionAlbum.objects.get(id=session_album_id)
            images = Img.objects.filter(SessionAlbum=session_album)

            paginator = self.pagination_class()
            paginated_images = paginator.paginate_queryset(images, request)

            serializer = ImgSerializer(paginated_images, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SessionAlbum.DoesNotExist:
            return Response({'error': 'SessionAlbum not found'}, status=status.HTTP_404_NOT_FOUND)



class CreateVideosView(APIView):
    def post(self, request, *args, **kwargs):
        videos_data = request.data.get('videos', [])
        session_album_id = request.data.get('session_album')

        if not videos_data or not session_album_id:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        session_album = SessionAlbum.objects.filter(id=session_album_id).first()

        if not session_album:
            return Response({'error': 'Session album not found'}, status=status.HTTP_404_NOT_FOUND)

        videos = []
        for video_data in videos_data:
            original_url = video_data.get('original')
            transformed_url = video_data.get('transformed')

            if not original_url or not transformed_url:
                return Response({'error': 'Invalid video data'}, status=status.HTTP_400_BAD_REQUEST)

            video = Video(video=original_url, WatermarkedVideo=transformed_url, SessionAlbum=session_album)
            video.save()
            videos.append(video)

        serializer = VideoSerializer(videos, many=True)
        return Response({'message': 'Videos created successfully', 'videos': serializer.data}, status=status.HTTP_201_CREATED)





@api_view(['GET'])
def get_waves_for_session_album(request, session_album_id):
    try:
        waves = Wave.objects.filter(session_album=session_album_id)
        
        # Paginate the queryset
        paginator = CustomPageNumberPagination()
        paginated_waves = paginator.paginate_queryset(waves, request)
        
        # Serialize the paginated data
        serializer = WaveSerializer(paginated_waves, many=True)
        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
    
    except Wave.DoesNotExist:
        return Response({'message': 'No waves found for the provided SessionAlbum ID.'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
def get_waves(request):
    try:
        wave_ids = request.data.get('waveIds', [])

        if not wave_ids:
            return Response({'error': 'No wave IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the wave objects based on the provided IDs
        waves = Wave.objects.filter(id__in=wave_ids)

        # Serialize the wave objects
        serializer = WaveSerializer(waves, many=True)

        return Response({'waves': serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


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
    



@api_view(['GET'])
def get_original_videos(request, session_album_id):
    session_album = get_object_or_404(SessionAlbum, id=session_album_id)
    videos = Video.objects.filter(SessionAlbum=session_album).values('video')
    original_videos = [video['video'] for video in videos if video['video']]
    return Response(original_videos)

@api_view(['GET'])
def get_watermarked_videos(request, session_album_id):
    session_album = get_object_or_404(SessionAlbum, id=session_album_id)
    videos = Video.objects.filter(SessionAlbum=session_album).values('WatermarkedVideo')
    WatermarkedVideos = [video['WatermarkedVideo'] for video in videos if video['WatermarkedVideo']]
    return Response(WatermarkedVideos)

@api_view(['GET'])
def get_videos_by_session(request, session_album_id):
    session_album = get_object_or_404(SessionAlbum, id=session_album_id)
    videos = Video.objects.filter(SessionAlbum=session_album)

    paginator = CustomPageNumberPagination()
    paginated_videos = paginator.paginate_queryset(videos, request)

    serializer = VideoSerializer(paginated_videos, many=True)
    return paginator.get_paginated_response(serializer.data)










