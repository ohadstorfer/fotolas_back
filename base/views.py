# views.py
from datetime import timedelta
import json
from urllib import request
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response

from base.pagination import CustomPageNumberPagination
from .models import DefaultAlbumsPricesForImages, DefaultAlbumsPricesForVideos, AlbumsPrices, AlbumsPricesForVideos, Chat, CustomUser, Message, Photographer, Purchase, PurchaseItem, Spot, SessionAlbum, Img, SpotLike, Follower, Video, Wave
from .serializers import  DefaultAlbumsPricesForImagesSerializer, DefaultAlbumsPricesForVideosSerializer, AlbumsPricesForVideosSerializer, AlbumsPricesSerializer, ChatSerializer, CustomUserSerializer, MessageSerializer, MyTokenObtainPairSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, PhotographerSerializer, PurchaseItemSerializer, PurchaseSerializer, SessionAlbumByPhotographerSerializer, SessionAlbumBySpotSerializer, SessionAlbumWithDetailsSerializer, SpotSerializer, SessionAlbumSerializer, ImgSerializer, SpotLikeSerializer, FollowerSerializer, VideoSerializer, WaveSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)

            # Generate a JWT token
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # Build reset URL
            reset_url = f"{settings.FRONTEND_URL}/reset-password/?token={token}"

            # Send reset email
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        new_access_token = str(token.access_token)
        return Response({"access": new_access_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ValidateTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []  # No permissions required to validate token

    def get(self, request):
        # If the request is authenticated, this method will be called
        return Response({'valid': True, 'detail': 'Token is valid.'}, status=status.HTTP_200_OK)




    

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

        # Create default album prices for images
        DefaultAlbumsPricesForImages.objects.create(
            photographer=photographer,
            price_1_to_5=20,
            price_6_to_50=25,
            price_51_plus=30
        )

        # Create default album prices for videos
        DefaultAlbumsPricesForVideos.objects.create(
            photographer=photographer,
            price_1_to_3=25,
            price_4_to_15=30,
            price_16_plus=35
        )



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
        # Get the count of SessionAlbums associated with the photographer
        session_album_count = SessionAlbum.objects.filter(photographer=photographer, active=True).count()

        # Get the count of unique Spots associated with the photographer's SessionAlbums
        unique_spots_count = SessionAlbum.objects.filter(photographer=photographer).values('spot').distinct().count()

        # Serialize the photographer data
        serializer = self.get_serializer(photographer)
        data = serializer.data

        # Add additional data to the response
        data['photographer_name'] = photographer_name
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Extract the user ID from the token
        token_user_id = request.user.id
        # Get the user_id from the request URL
        user_id = self.kwargs['user_id']

        # Ensure the user_id from the URL matches the user from the token
        if str(token_user_id) != str(user_id):
            raise PermissionDenied("You are not authorized to view this photographer's details.")

        # Get the photographer object based on the user_id
        photographer = get_object_or_404(Photographer, user__id=user_id)

        # Get the photographer's full name and other additional data
        photographer_name = photographer.user.get_full_name()
        session_album_count = SessionAlbum.objects.filter(photographer=photographer, active=True).count()
        unique_spots_count = SessionAlbum.objects.filter(photographer=photographer).values('spot').distinct().count()

        # Serialize the photographer data
        serializer = self.get_serializer(photographer)
        data = serializer.data

        # Add the extra fields
        data['photographer_name'] = photographer_name
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
            purchased_images = []
            purchased_videos = []

            for purchase in purchases:
                # Get the related SessionAlbum and calculate the days left until expiration
                session_album = purchase.SessionAlbum
                days_left = None
                if session_album and session_album.expiration_date:
                    days_left = (session_album.expiration_date - timezone.now()).days

                purchase_items = PurchaseItem.objects.filter(PurchaseId=purchase.id)

                # Gather images
                for item in purchase_items:
                    if item.Img:
                        purchased_images.append({
                            'id': item.Img.id,
                            'photo': item.Img.photo,
                            'WatermarkedPhoto': item.Img.WatermarkedPhoto,
                            'days_until_expiration': days_left,  # Add days left
                            # Add other fields as necessary
                        })

                    # Gather videos
                    if item.Video:
                        purchased_videos.append({
                            'id': item.Video.id,
                            'video': item.Video.video,
                            'WatermarkedVideo': item.Video.WatermarkedVideo,
                            'days_until_expiration': days_left,  # Add days left
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
    


from django.utils import timezone
from django.db.models import Case, When, F, ExpressionWrapper, DurationField



class SessionAlbumListAPIView(generics.ListAPIView):
    serializer_class = SessionAlbumWithDetailsSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        now = timezone.now()
        # Filter for active SessionAlbums and calculate expiration date
        queryset = SessionAlbum.objects.filter(active=True).annotate(
            calculated_expiration_date=Case(
                When(videos=True, then=F('created_at') + timedelta(days=5)),
                When(videos=False, then=F('created_at') + timedelta(days=30)),
                default=None
            )
        )

        # Calculate remaining days until expiration
        queryset = queryset.annotate(
            days_until_expiration=F('calculated_expiration_date') - now
        ).filter(days_until_expiration__gte=timedelta(days=0)).order_by('-id')

        return queryset







class SessionAlbumDetailByIDAPIView(generics.RetrieveAPIView):
    serializer_class = SessionAlbumWithDetailsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return SessionAlbum.objects.filter(active=True)

# class SessionAlbumDetailByIDAPIView(generics.RetrieveAPIView):
#     serializer_class = SessionAlbumWithDetailsSerializer
#     lookup_field = 'id'

#     def get_queryset(self):
#         # Ensure the album is active and not expired
#         return SessionAlbum.objects.filter(active=True, expiration_date__gte=timezone.now())




class SessionAlbumByPhotographer(generics.ListAPIView):
    serializer_class = SessionAlbumByPhotographerSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        photographer_id = self.kwargs['photographer_id']  # Assuming the photographer_id is passed as a URL parameter
        now = timezone.now()
        # Create a queryset that filters active albums for the specified photographer
        queryset = SessionAlbum.objects.filter(
            photographer__id=photographer_id,
            active=True
        ).annotate(
            calculated_expiration_date=Case(
                When(videos=True, then=F('created_at') + timedelta(days=5)),
                When(videos=False, then=F('created_at') + timedelta(days=30)),
                default=None
            )
        ).filter(calculated_expiration_date__gte=now)  # Filter to ensure sessions are not expired
        return queryset.order_by('-id')





class SessionAlbumBySpot(generics.ListAPIView):
    serializer_class = SessionAlbumBySpotSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        spot_id = self.kwargs['spot_id']  # Assuming the spot_id is passed as a URL parameter
        now = timezone.now()
        # Create a queryset that filters active albums for the specified spot
        queryset = SessionAlbum.objects.filter(
            spot__id=spot_id,
            active=True
        ).annotate(
            calculated_expiration_date=Case(
                When(videos=True, then=F('created_at') + timedelta(days=5)),
                When(videos=False, then=F('created_at') + timedelta(days=30)),
                default=None
            )
        ).filter(calculated_expiration_date__gte=now)  # Filter to ensure sessions are not expired
        return queryset.order_by('-id')




class DeactivateSessionAlbum(generics.UpdateAPIView):
    queryset = SessionAlbum.objects.all()
    serializer_class = SessionAlbumSerializer
    # permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def put(self, request, *args, **kwargs):
        # Get the SessionAlbum object based on the session_album_id from URL
        session_album = self.get_object()

        if session_album:
            # Deactivate the SessionAlbum
            session_album.active = False
            session_album.save()

            return Response({"detail": "Session album has been deactivated."}, status=status.HTTP_200_OK)
        else:
            # Return a 404 response if the SessionAlbum does not exist
            return Response({"detail": "Session album not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self):
        # Get the session_album_id from the URL parameters
        session_album_id = self.kwargs['session_album_id']
        return self.queryset.filter(id=session_album_id).first()




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





class DefaultAlbumsPricesForImagesCreateView(generics.CreateAPIView):
    """
    View to create default album prices for images.
    Requires the user to be authenticated.
    """
    queryset = DefaultAlbumsPricesForImages.objects.all()
    serializer_class = DefaultAlbumsPricesForImagesSerializer
    
class DefaultAlbumsPricesForImagesUpdateView(generics.UpdateAPIView):
    """
    View to update default album prices for images by photographer ID.
    Requires the user to be authenticated.
    """
    serializer_class = DefaultAlbumsPricesForImagesSerializer
    
    def get_object(self):
        # Get photographer ID from URL
        photographer_id = self.kwargs.get('photographer_id')
        
        # Try to find the object related to the given photographer ID
        obj = DefaultAlbumsPricesForImages.objects.filter(photographer__id=photographer_id).first()
        
        # Return None or handle what to do if the object doesn't exist
        if obj:
            return obj
        else:
            return None  # or handle this case appropriately (e.g., return an empty response)
        



class DefaultAlbumsPricesForImagesListView(generics.ListAPIView):
    """
    View to retrieve default album prices for images by photographer ID.
    Requires the user to be authenticated.
    """
    serializer_class = DefaultAlbumsPricesForImagesSerializer

    def get_queryset(self):
        photographer_id = self.kwargs['photographer_id']
        return DefaultAlbumsPricesForImages.objects.filter(photographer_id=photographer_id)

class DefaultAlbumsPricesForVideosCreateView(generics.CreateAPIView):
    """
    View to create default album prices for videos.
    Requires the user to be authenticated.
    """
    queryset = DefaultAlbumsPricesForVideos.objects.all()
    serializer_class = DefaultAlbumsPricesForVideosSerializer
    


class DefaultAlbumsPricesForVideosUpdateView(generics.UpdateAPIView):
    """
    View to update default album prices for videos by photographer ID.
    Requires the user to be authenticated.
    """
    serializer_class = DefaultAlbumsPricesForVideosSerializer
    
    def get_object(self):
        # Get photographer ID from URL
        photographer_id = self.kwargs.get('photographer_id')
        
        # Try to find the object related to the given photographer ID
        obj = DefaultAlbumsPricesForVideos.objects.filter(photographer__id=photographer_id).first()
        
        # Return None or handle the case where the object doesn't exist
        if obj:
            return obj
        else:
            return None
        



class DefaultAlbumsPricesForVideosListView(generics.ListAPIView):
    """
    View to retrieve default album prices for videos by photographer ID.
    Requires the user to be authenticated.
    """
    serializer_class = DefaultAlbumsPricesForVideosSerializer
    

    def get_queryset(self):
        photographer_id = self.kwargs['photographer_id']
        return DefaultAlbumsPricesForVideos.objects.filter(photographer_id=photographer_id)




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

from rest_framework.permissions import IsAuthenticated

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

    # Get file types from query parameters
    file_types_param = request.GET.get('file_types', '')
    if not file_types_param:
        return JsonResponse({'error': 'No file types provided'}, status=400)

    # Convert file_types to a list
    file_types = file_types_param.split(',')
    
    # Generate presigned URLs for each file type
    presigned_urls = []
    for file_type in file_types:
        # Determine file extension based on MIME type
        extension = ''
        if file_type == 'video/mp4':
            extension = 'mp4'
        elif file_type == 'video/webm':
            extension = 'webm'
        elif file_type == 'video/quicktime':
            extension = 'mov'
        else:
            continue  # Skip unsupported types

        unique_filename = f'{uuid.uuid4()}.{extension}'
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': 'surfingram-original-video', 'Key': unique_filename},
            ExpiresIn=3600  # URL expiration time in seconds
        )
        presigned_urls.append(presigned_url)

    if not presigned_urls:
        return JsonResponse({'error': 'No valid file types provided'}, status=400)

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



    # Validate session_album_id
    if not session_album_id:
        return Response({'error': 'Session album ID is required'}, status=status.HTTP_400_BAD_REQUEST)

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
        session_album.set_expiration_date()
        session_album.save()

        return Response({'message': 'Images created successfully without waves'}, status=status.HTTP_201_CREATED)
    




    # Check if all EXIF dates are identical
    if len(set(exif_dates)) == 1:  # If all EXIF dates are identical
        # If all EXIF dates are the same, create images without waves
        images_to_create = [
            Img(photo=original_url, WatermarkedPhoto=watermarked_url, SessionAlbum_id=session_album_id)
            for original_url, watermarked_url in zip(original_urls, watermarked_urls)
        ]
        Img.objects.bulk_create(images_to_create)
        
        # Mark the SessionAlbum as active but not divided into waves
        session_album = SessionAlbum.objects.get(id=session_album_id)
        session_album.dividedToWaves = False
        session_album.active = True
        session_album.set_expiration_date()
        session_album.save()

        return Response({'message': 'Images created successfully without waves'}, status=status.HTTP_201_CREATED)
    
    

    images_and_waves = []
    current_wave = None
    previous_datetime = None
    TIME_GAP_THRESHOLD = 3  # seconds

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
        session_album.set_expiration_date()
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
            session_album.active = True
            session_album.set_expiration_date()
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


    session_album.active = True
    session_album.set_expiration_date()  # Assuming this method sets some expiration logic
    session_album.save()

    # Return the created video details
    return Response({
        "message": "Videos created successfully",
        "created_videos": [video.id for video in created_videos]
    }, status=status.HTTP_201_CREATED)













class CreateVideosView(APIView):
    def post(self, request, *args, **kwargs):
        videos_data = request.data.get('videos', [])
        session_album_id = request.data.get('session_album')

        if not videos_data or not session_album_id:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch session album once
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

        # Use the already fetched session_album instance
        session_album = SessionAlbum.objects.get(id=session_album_id)
        session_album.active = True
        session_album.set_expiration_date()
        session_album.save()

        serializer = VideoSerializer(videos, many=True)
        return Response({'message': 'Videos created successfully', 'videos': serializer.data}, status=status.HTTP_201_CREATED)
    




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
    


@csrf_exempt
def get_images_by_ids(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_ids = data.get('image_ids', [])
            
            if not image_ids:
                return JsonResponse({"error": "No image IDs provided"}, status=400)
            
            images = Img.objects.filter(id__in=image_ids).values('id', 'photo')
            return JsonResponse(list(images), safe=False)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_videos_by_ids(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            video_ids = data.get('video_ids', [])
            
            if not video_ids:
                return JsonResponse({"error": "No video IDs provided"}, status=400)
            
            videos = Video.objects.filter(id__in=video_ids).values('id', 'video')
            return JsonResponse(list(videos), safe=False)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)






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












from decouple import config
import stripe
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import JsonResponse

# Set Stripe API key and version
stripe.api_key = config('STRIPE_API_KEY')
stripe.api_version = '2023-10-16'

@csrf_exempt
@require_POST
def create_account_link(request):
    try:
        data = json.loads(request.body)
        connected_account_id = data.get("account")

        account_link = stripe.AccountLink.create(
            account=connected_account_id,
            return_url=f"https://surfpik.com/VerificationProccess",
            refresh_url=f"https://surfpik.com/RefreshURL",
            type="account_onboarding",
        )

        return JsonResponse({"url": account_link.url})
    except Exception as e:
        print("Error creating account link: ", e)
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def create_account(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        
        # Get the country and user ID from the parsed data
        selectedCountry = data.get('Country')
        user_id = data.get('user_id')  # Get the user ID from the request

        if not selectedCountry:
            return JsonResponse({"error": "Country is required"}, status=400)
        
        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)

        # Get the user instance based on the user_id
        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Prepare the account creation parameters
        account_params = {
            "type": "express",
            "capabilities": {
                "transfers": {"requested": True},
            },
            "business_type": "individual",  # Set this according to your requirements
            "country": selectedCountry,
        }
        
        # If the country is not "us", include the tos_acceptance field
        if selectedCountry.lower() != "us":
            account_params["tos_acceptance"] = {"service_agreement": "recipient"}
        
        # Create the Stripe account
        account = stripe.Account.create(**account_params)

        # Update the user with the new Stripe account ID and initial verification status
        user.stripe_account_id = account.id
        user.verification_status = 'Pending Verification'  # Initial status
        user.save()

        return JsonResponse({"account": account.id})
    
    except Exception as e:
        print("Error creating account: ", e)
        return JsonResponse({"error": str(e)}, status=500)





endpoint_secret = config('endpoint_secret')





@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'account.updated':
        account = event['data']['object']
        handle_account_update(account)

    return JsonResponse({'success': True})

def handle_account_update(account):
    stripe_account_id = account.get('id')
    disabled_reason = account.get('requirements', {}).get('disabled_reason')

    user = CustomUser.objects.filter(stripe_account_id=stripe_account_id).first()
    if user:
        if disabled_reason is None:
            user.verification_status = 'Verified'
            user.is_photographer = True
            user.save()

            # Create Photographer instance if it doesn't exist and set the stripe_account_id
            photographer, created = Photographer.objects.get_or_create(user=user, stripe_account_id=stripe_account_id)

            # Create default pricing for images and videos
            if created:
                # Default pricing for images
                DefaultAlbumsPricesForImages.objects.create(
                    photographer=photographer,
                    price_1_to_5=20.0,
                    price_6_to_50=25.0,
                    price_51_plus=30.0
                )

                # Default pricing for videos
                DefaultAlbumsPricesForVideos.objects.create(
                    photographer=photographer,
                    price_1_to_3=25.0,
                    price_4_to_15=30.0,
                    price_16_plus=35.0
                )

        else:
            user.verification_status = f'Disabled: {disabled_reason}'
            user.save()

        print(f'Updated verification status for user {user.email}: {user.verification_status}')








@csrf_exempt
@require_POST
def create_checkout_session(request):
    try:
        # Parse the incoming JSON request body
        data = json.loads(request.body.decode('utf-8'))
        
        # Extract details from the request data
        product_name = data.get('product_name', 'Default Product')
        amount = data.get('amount', 1000)  # Default to $10.00 (in cents)
        currency = data.get('currency', 'usd')
        quantity = data.get('quantity', 1)
        connected_account_id = data.get('connected_account_id')

        # Validate required fields
        if not connected_account_id:
            return JsonResponse({"error": "Connected account ID is required"}, status=400)

        # Create the checkout session
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {"name": product_name},
                        "unit_amount": amount,
                    },
                    "quantity": quantity,
                },
            ],
            payment_intent_data={
                "application_fee_amount": int(amount * 0.2) + 100,
                "transfer_data": {"destination": connected_account_id},
            },
            mode="payment",
            success_url="https://surfpik.com/PaymentSuccessfull",
            cancel_url="https://surfpik.com/CartErrors",
        )

        return JsonResponse({"url": session.url})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)









@csrf_exempt
def create_account_session(request):
    try:
        # Check if the request method is POST
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        # Parse JSON body to retrieve connected account ID
        body = json.loads(request.body.decode('utf-8'))
        connected_account_id = body.get('connected_account_id')

        if not connected_account_id:
            return JsonResponse({'error': 'Connected account ID is required'}, status=400)

        # Create the account session
        account_session = stripe.AccountSession.create(
            account=connected_account_id,
            components={
                "payments": {
                    "enabled": True,
                        "features": {
                            "refund_management": False,
                            "dispute_management": False,
                            "capture_payments": False,
                            "destination_on_behalf_of_charge_management": False,
                        },
                    },
                "balances": {
                    "enabled": True,
                    "features": {
                        "instant_payouts": False,
                        "standard_payouts": False,
                        "edit_payout_schedule": False,
                    },
                    },
            },
        )

        return JsonResponse({
            'client_secret': account_session.client_secret,
        })

    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account session: ', e)
        return JsonResponse({'error': str(e)}, status=500)
    








@csrf_exempt
def create_account_session_for_alerts(request):
    try:
        # Check if the request method is POST
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        # Parse JSON body to retrieve connected account ID
        body = json.loads(request.body.decode('utf-8'))
        connected_account_id = body.get('connected_account_id')

        if not connected_account_id:
            return JsonResponse({'error': 'Connected account ID is required'}, status=400)

        # Create the account session
        account_session = stripe.AccountSession.create(
            account=connected_account_id,
            components={
                "notification_banner": {
                "enabled": True,
                "features": {"external_account_collection": True},
                },
                "account_management": {
                "enabled": True,
                "features": {"external_account_collection": True},
                },
            },
        )

        return JsonResponse({
            'client_secret': account_session.client_secret,
        })

    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account session: ', e)
        return JsonResponse({'error': str(e)}, status=500)
    


