# views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlbumsPrices, Chat, CustomUser, Message, Photographer, Spot, SessionAlbum, PersonalAlbum, Img, CensoredImg, SpotLike, Follower, Order
from .serializers import AlbumsPricesSerializer, ChatSerializer, CustomUserSerializer, ImgByPersonalAlbumSerializer, MessageSerializer, MyTokenObtainPairSerializer, PhotographerSerializer, SessionAlbumByPhotographerSerializer, SessionAlbumBySpotSerializer, SessionAlbumWithDetailsSerializer, SpotSerializer, SessionAlbumSerializer, PersonalAlbumSerializer, ImgSerializer, CensoredImgSerializer, SpotLikeSerializer, FollowerSerializer, OrderSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    
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
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer




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





class PersonalAlbumListCreateView(generics.ListCreateAPIView):
    queryset = PersonalAlbum.objects.all()
    serializer_class = PersonalAlbumSerializer

class PersonalAlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalAlbum.objects.all()
    serializer_class = PersonalAlbumSerializer





class ImgListCreateView(generics.ListCreateAPIView):
    queryset = Img.objects.all()
    serializer_class = ImgSerializer

class ImgDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Img.objects.all()
    serializer_class = ImgSerializer





class CensoredImgListCreateView(generics.ListCreateAPIView):
    queryset = CensoredImg.objects.all()
    serializer_class = CensoredImgSerializer

class CensoredImgDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CensoredImg.objects.all()
    serializer_class = CensoredImgSerializer





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




class CreateAlbumView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a Session Album, Personal Album, and Images.
        """
        session_album_data = request.data.get('session_album', {})
        personal_albums_data = request.data.get('personal_albums', [])
        images_data = request.data.get('images', [])

        session_album_serializer = SessionAlbumSerializer(data=session_album_data)
        if session_album_serializer.is_valid():
            session_album = session_album_serializer.save()
        else:
            return Response(session_album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        personal_albums = []
        for personal_album_data in personal_albums_data:
            personal_album_data['session_album'] = session_album.id
            personal_album_serializer = PersonalAlbumSerializer(data=personal_album_data)
            if personal_album_serializer.is_valid():
                personal_album = personal_album_serializer.save()
                personal_albums.append(personal_album)
            else:
                session_album.delete()
                return Response(personal_album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for personal_album in personal_albums:
            for image_data in images_data:
                image_data['personal_album'] = personal_album.id
                image_serializer = ImgSerializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    session_album.delete()
                    for album in personal_albums:
                        album.delete()
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Album created successfully."}, status=status.HTTP_201_CREATED)
    


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




class AlbumsPricesListCreateView(generics.ListCreateAPIView):
    queryset = AlbumsPrices.objects.all()
    serializer_class = AlbumsPricesSerializer

class AlbumsPricesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlbumsPrices.objects.all()
    serializer_class = AlbumsPricesSerializer





class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer







class ImgByPersonalAlbumListView(generics.ListAPIView):
    serializer_class = ImgByPersonalAlbumSerializer

    def get_queryset(self):
        personal_album_id = self.kwargs['personal_album_id']
        return Img.objects.filter(personal_album__id=personal_album_id)
    




    
    



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


class PersonalAlbumListView(generics.ListAPIView):
    serializer_class = PersonalAlbumSerializer

    def get_queryset(self):
        session_album_id = self.kwargs['session_album_id']
        personal_albums = PersonalAlbum.objects.filter(session_album_id=session_album_id)
        return personal_albums

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add image count to serializer context
        session_album_id = self.kwargs['session_album_id']
        context['image_counts'] = {album.id: album.img_set.count() for album in self.get_queryset()}
        return context



