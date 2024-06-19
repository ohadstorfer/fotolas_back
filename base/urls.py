# urls.py
from django import views
from django.urls import path
from .views import (
     AlbumsPricesDetailView, AlbumsPricesListCreateView, ChatDetailView, ChatListCreateView, CustomUserListCreateView, CustomUserDetailView, FollowersByPhotographerListView, FollowersByUserListView, MessageDetailView, MessageListCreateView, MyTokenObtainPairView, PhotographerByUserIdView, 
    PhotographerListCreateView, PhotographerDetailView, SessionAlbumByPhotographer, SessionAlbumBySpot, SessionAlbumListAPIView, SpotLikesBySpotListView, SpotLikesByUserListView,
    SpotListCreateView, SpotDetailView,
    SessionAlbumListCreateView, SessionAlbumDetailView,
    ImgListCreateView, ImgDetailView,
    SpotLikeListCreateView, SpotLikeDetailView,
    FollowerListCreateView, FollowerDetailView,
    OrderListCreateView, OrderDetailView, create_images_and_waves, get_batch_presigned_urlssss, get_images_for_multiple_waves, get_images_for_wave, get_watermarked_photos_by_wave, get_waves_for_session_album, 
)

urlpatterns = [

    
    path('custom-users/', CustomUserListCreateView.as_view(), name='custom-user-list-create'),
    path('custom-users/<int:pk>/', CustomUserDetailView.as_view(), name='custom-user-detail'),

    path('photographers/', PhotographerListCreateView.as_view(), name='photographer-list-create'),
    path('photographers/<int:pk>/', PhotographerDetailView.as_view(), name='photographer-detail'),
    path('photographer/by_user/<int:user_id>/', PhotographerByUserIdView.as_view(), name='photographer_by_user'),

    path('spots/', SpotListCreateView.as_view(), name='spot-list-create'),
    path('spots/<int:pk>/', SpotDetailView.as_view(), name='spot-detail'),

    path('session-albums/', SessionAlbumListCreateView.as_view(), name='session-album-list-create'),
    path('session-albums/<int:pk>/', SessionAlbumDetailView.as_view(), name='session-album-detail'),


    path('img/', ImgListCreateView.as_view(), name='img-list-create'),
    path('img/<int:pk>/', ImgDetailView.as_view(), name='img-detail'),
   

    path('spot-likes/', SpotLikeListCreateView.as_view(), name='spot-like-list-create'),
    path('spot-likes/<int:pk>/', SpotLikeDetailView.as_view(), name='spot-like-detail'),

    path('users/<int:user_id>/spot-likes/', SpotLikesByUserListView.as_view(), name='spot-likes-by-user'),
    path('spots/<int:spot_id>/spot-likes/', SpotLikesBySpotListView.as_view(), name='spot-likes-by-spot'),

    path('followers/', FollowerListCreateView.as_view(), name='follower-list-create'),
    path('followers/<int:pk>/', FollowerDetailView.as_view(), name='follower-detail'),

    path('users/<int:user_id>/followers/', FollowersByUserListView.as_view(), name='followers-by-user'),
    path('photographers/<int:photographer_id>/followers/', FollowersByPhotographerListView.as_view(), name='followers-by-photographer'),
    
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),


     path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),

    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),



    path('session-albums-with-details/', SessionAlbumListAPIView.as_view(), name='session-album-list'),
    path('session-albums-by-photographer/<int:photographer_id>/', SessionAlbumByPhotographer.as_view(), name='session-album-by-photographer'),
    path('session-albums-by-spot/<int:spot_id>/', SessionAlbumBySpot.as_view(), name='session-album-by-spot'),


    path('albums_prices/', AlbumsPricesListCreateView.as_view(), name='albums-prices-list-create'),
    path('albums_prices/<int:pk>/', AlbumsPricesDetailView.as_view(), name='albums-prices-detail'),
  

    path('api/get_batch_presigned_urlssss', get_batch_presigned_urlssss, name='get_batch_presigned_urlssss'),

    path('api/create_images_and_waves/', create_images_and_waves, name='create_images_and_waves'),

    path('waves/<int:session_album_id>/', get_waves_for_session_album, name='waves-for-session-album'),

    path('images/<int:wave_id>/', get_images_for_wave, name='images-for-wave'),

    path('api/get_images_for_multiple_waves/', get_images_for_multiple_waves, name='get_images_for_multiple_waves'),

    path('watermarked_photos/<int:wave_id>/', get_watermarked_photos_by_wave, name='get_watermarked_photos_by_wave'),

]