# urls.py
from django.urls import path
from .views import (
    AlbumsPricesDetailView, AlbumsPricesListCreateView, ChatDetailView, ChatListCreateView, CreateAlbumView, CustomUserListCreateView, CustomUserDetailView, FollowersByPhotographerListView, FollowersByUserListView, ImgByPersonalAlbumListView, ImgListCreateBulkView, MessageDetailView, MessageListCreateView, MyTokenObtainPairView, PersonalAlbumListView, PhotographerByUserIdView, 
    PhotographerListCreateView, PhotographerDetailView, SessionAlbumByPhotographer, SessionAlbumBySpot, SessionAlbumListAPIView, SpotLikesBySpotListView, SpotLikesByUserListView,
    SpotListCreateView, SpotDetailView,
    SessionAlbumListCreateView, SessionAlbumDetailView,
    PersonalAlbumListCreateView, PersonalAlbumDetailView,
    ImgListCreateView, ImgDetailView,
    CensoredImgListCreateView, CensoredImgDetailView,
    SpotLikeListCreateView, SpotLikeDetailView,
    FollowerListCreateView, FollowerDetailView,
    OrderListCreateView, OrderDetailView, update_prices_view,
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

    path('personal-albums/', PersonalAlbumListCreateView.as_view(), name='personal-album-list-create'),
    path('personal-albums/<int:pk>/', PersonalAlbumDetailView.as_view(), name='personal-album-detail'),

    path('img/', ImgListCreateView.as_view(), name='img-list-create'),
    path('img/<int:pk>/', ImgDetailView.as_view(), name='img-detail'),
    path('create_personal_albums_and_images/', ImgListCreateBulkView.as_view(), name='create_personal_albums_and_images'),

    path('censored-img/', CensoredImgListCreateView.as_view(), name='censored-img-list-create'),
    path('censored-img/<int:pk>/', CensoredImgDetailView.as_view(), name='censored-img-detail'),

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

    path('create-album/', CreateAlbumView.as_view(), name='create-album'),

     path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),

    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/img/by_personal_album/<int:personal_album_id>/', ImgByPersonalAlbumListView.as_view(), name='img_by_personal_album'),

    path('personal-albums-by-sess/<int:session_album_id>/', PersonalAlbumListView.as_view(), name='personal-album-list'),

    path('session-albums-with-details/', SessionAlbumListAPIView.as_view(), name='session-album-list'),
    path('session-albums-by-photographer/<int:photographer_id>/', SessionAlbumByPhotographer.as_view(), name='session-album-by-photographer'),
    path('session-albums-by-spot/<int:spot_id>/', SessionAlbumBySpot.as_view(), name='session-album-by-spot'),

    path('update_prices/<int:session_album_id>/', update_prices_view, name='update_prices'),

    path('albums_prices/', AlbumsPricesListCreateView.as_view(), name='albums_prices-list-create'),
    path('albums_prices/<int:pk>/', AlbumsPricesDetailView.as_view(), name='albums_prices-detail'),


]