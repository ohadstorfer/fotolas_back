# urls.py
from django import views
from django.urls import path
from .views import (
     AlbumsPricesBySess, AlbumsPricesDetailView, AlbumsPricesForVideosBySess, AlbumsPricesForVideosDetailView, AlbumsPricesForVideosListCreateView, AlbumsPricesListCreateView, ChatDetailView, ChatListCreateView, CreatePurchaseView, CreatePurchaseWithImagesView, CreatePurchaseWithVideosView, CreatePurchaseWithWavesView, CreateVideoPerAlbums, CreateVideosView, CustomUserListCreateView, CustomUserDetailView, FollowersByPhotographerListView, FollowersByUserListView,  GetImagesBySessionAlbumView, GetPurchasedItemsBySurfer, GetPurchasesByPhotographerName, MessageDetailView, MessageListCreateView, MyTokenObtainPairView, PasswordResetRequestView, PasswordResetView, PhotographerByUserIdView, PhotographerDetailUpdateView, 
    PhotographerListCreateView, PhotographerDetailView, PurchaseDetailView, PurchaseItemDetailView, PurchaseItemListCreateView, PurchaseListCreateView, PurchasesByPhotographerView, PurchasesBySurferView, SessionAlbumByPhotographer, SessionAlbumBySpot, SessionAlbumDetailByIDAPIView, SessionAlbumListAPIView, SpotLikesBySpotListView, SpotLikesByUserListView,
    SpotListCreateView, SpotDetailView,
    SessionAlbumListCreateView, SessionAlbumDetailView,
    ImgListCreateView, ImgDetailView,
    SpotLikeListCreateView, SpotLikeDetailView,
    FollowerListCreateView, FollowerDetailView, ValidateTokenView,
    DefaultAlbumsPricesForImagesCreateView, DefaultAlbumsPricesForImagesUpdateView, DefaultAlbumsPricesForImagesListView,  DefaultAlbumsPricesForVideosCreateView, DefaultAlbumsPricesForVideosUpdateView, DefaultAlbumsPricesForVideosListView, create_account, create_account_link, create_account_session, create_account_session_for_alerts, create_checkout_session,
    create_images_and_waves, create_videos, get_batch_presigned_urlssss, get_images_by_ids, get_images_for_multiple_waves, get_images_for_wave, DeactivateSessionAlbum,  get_original_videos, get_videos_by_ids, get_videos_by_session, get_watermarked_photos_by_wave, get_watermarked_videos, get_waves, get_waves_for_session_album, invoke_lambda_view, presigned_urls_for_original_videos, presigned_urls_for_originals, presigned_urls_for_profile_pictures, presigned_urls_for_watermarked, presigned_urls_for_watermarked_videos, stripe_webhook, stripe_webhook_invoke_lambda, test_webhook_invoke_lambda, 
)

urlpatterns = [

    
    path('custom-users/', CustomUserListCreateView.as_view(), name='custom-user-list-create'),
    path('custom-users/<int:pk>/', CustomUserDetailView.as_view(), name='custom-user-detail'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('validate-token/', ValidateTokenView.as_view(), name='validate-token'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),

    path('photographers/', PhotographerListCreateView.as_view(), name='photographer-list-create'),
    path('update-photographers/<int:pk>/', PhotographerDetailUpdateView.as_view(), name='photographer-detail-update'),
    path('photographers/<int:pk>/', PhotographerDetailView.as_view(), name='photographer-detail'),
    path('photographer/by_user/<int:user_id>/', PhotographerByUserIdView.as_view(), name='photographer_by_user'),

    path('spots/', SpotListCreateView.as_view(), name='spot-list-create'),
    path('spots/<int:pk>/', SpotDetailView.as_view(), name='spot-detail'),

    path('session-albums/', SessionAlbumListCreateView.as_view(), name='session-album-list-create'),
    path('session-albums/<int:pk>/', SessionAlbumDetailView.as_view(), name='session-album-detail'),


    path('img/', ImgListCreateView.as_view(), name='img-list-create'),
    path('img/<int:pk>/', ImgDetailView.as_view(), name='img-detail'),
    path('session_album/<int:session_album_id>/images/', GetImagesBySessionAlbumView.as_view(), name='get_images_by_session_album'),
   

    path('spot-likes/', SpotLikeListCreateView.as_view(), name='spot-like-list-create'),
    path('spot-likes/<int:pk>/', SpotLikeDetailView.as_view(), name='spot-like-detail'),

    path('users/<int:user_id>/spot-likes/', SpotLikesByUserListView.as_view(), name='spot-likes-by-user'),
    path('spots/<int:spot_id>/spot-likes/', SpotLikesBySpotListView.as_view(), name='spot-likes-by-spot'),

    path('followers/', FollowerListCreateView.as_view(), name='follower-list-create'),
    path('followers/<int:pk>/', FollowerDetailView.as_view(), name='follower-detail'),

    path('users/<int:user_id>/followers/', FollowersByUserListView.as_view(), name='followers-by-user'),
    path('photographers/<int:photographer_id>/followers/', FollowersByPhotographerListView.as_view(), name='followers-by-photographer'),
    
    path('Purchases/', PurchaseListCreateView.as_view(), name='Purchase-list-create'),
    path('Purchases/<int:pk>/', PurchaseDetailView.as_view(), name='Purchase-detail'),
    path('purchase-items/', PurchaseItemListCreateView.as_view(), name='purchase-item-list-create'),
    path('purchase-items/<int:pk>/', PurchaseItemDetailView.as_view(), name='purchase-item-detail'),
    path('create-purchase/', CreatePurchaseView.as_view(), name='create-purchase'),
    path('create-purchase-with-images/', CreatePurchaseWithImagesView.as_view(), name='create_purchase_with_images'),
    path('create-purchase-with-videos/', CreatePurchaseWithVideosView.as_view(), name='create_purchase_with_videos'),
    path('create-purchase-with-waves/', CreatePurchaseWithWavesView.as_view(), name='create-purchase-with-waves'),
    path('purchases/photographer/<int:photographer_userId>/', PurchasesByPhotographerView.as_view(), name='purchases-by-photographer'),
    path('purchases/surfer/<int:surfer_userId>/', PurchasesBySurferView.as_view(), name='purchases-by-surfer'),
    path('purchased-items-by-surfer/<int:surfer_id>/', GetPurchasedItemsBySurfer.as_view(), name='get-images-by-surfer-id'),
    path('purchases/photographer/<str:photographer_name>/', GetPurchasesByPhotographerName.as_view(), name='get-purchases-by-photographer-name'),


    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),

    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),




    path('session-albums-with-details/', SessionAlbumListAPIView.as_view(), name='session-album-list'),
    path('session-albums-with-details-by-id/<int:id>/', SessionAlbumDetailByIDAPIView.as_view(), name='session-albums-with-details-by-id'),
    path('session-albums-by-photographer/<int:photographer_id>/', SessionAlbumByPhotographer.as_view(), name='session-album-by-photographer'),
    path('session-albums-by-spot/<int:spot_id>/', SessionAlbumBySpot.as_view(), name='session-album-by-spot'),
    path('session-album/deactivate/<int:session_album_id>/', DeactivateSessionAlbum.as_view(), name='deactivate-session-album'),



    path('albums_prices/', AlbumsPricesListCreateView.as_view(), name='albums-prices-list-create'),
    path('albums_prices/<int:pk>/', AlbumsPricesDetailView.as_view(), name='albums-prices-detail'),
    path('albums-prices-by-sess/<int:session_album_id>/', AlbumsPricesBySess.as_view(), name='albums-prices-by-sess'),

    path('albums_prices-for-videos/', AlbumsPricesForVideosListCreateView.as_view(), name='albums-prices-list-create'),
    path('albums_prices-for-videos/<int:pk>/', AlbumsPricesForVideosDetailView.as_view(), name='albums-prices-detail'),
    path('albums-prices-for-videos-by-sess/<int:session_album_id>/', AlbumsPricesForVideosBySess.as_view(), name='albums-prices-by-sess'),

    path('default-album-prices/images/', DefaultAlbumsPricesForImagesCreateView.as_view(), name='create_default_album_prices_images'),
    path('default-album-prices-update/images/photographer/<int:photographer_id>/', DefaultAlbumsPricesForImagesUpdateView.as_view(), name='update_default_album_prices_images_by_photographer'),
    path('default-album-prices/images/photographer/<int:photographer_id>/', DefaultAlbumsPricesForImagesListView.as_view(), name='list_default_album_prices_images'),

    path('default-album-prices/videos/', DefaultAlbumsPricesForVideosCreateView.as_view(), name='create_default_album_prices_videos'),
    path('default-album-prices-update/videos/<int:photographer_id>/', DefaultAlbumsPricesForVideosUpdateView.as_view(), name='update_default_album_prices_videos'),
    path('default-album-prices/videos/photographer/<int:photographer_id>/', DefaultAlbumsPricesForVideosListView.as_view(), name='list_default_album_prices_videos'),

    path('api/get_batch_presigned_urlssss', get_batch_presigned_urlssss, name='get_batch_presigned_urlssss'),
    path('presigned_urls_for_originals', presigned_urls_for_originals, name='presigned_urls_for_originals'),
    path('presigned_urls_for_watermarked', presigned_urls_for_watermarked, name='presigned_urls_for_watermarked'),
    path('presigned_urls_for_original_videos', presigned_urls_for_original_videos, name='presigned_urls_for_original_videos'),
    path('presigned_urls_for_watermarked_videos', presigned_urls_for_watermarked_videos, name='presigned_urls_for_watermarked_videos'),
    path('presigned_urls_for_profile_pictures', presigned_urls_for_profile_pictures, name='presigned_urls_for_profile_pictures'),


    path('api/create_images_and_waves/', create_images_and_waves, name='create_images_and_waves'),
    path('create-multuple-videos/', create_videos, name='create-multuple-videos'),

    path('create_videos/', CreateVideosView.as_view(), name='create_videos'),
    path('create-videos-per-album/', CreateVideoPerAlbums.as_view(), name='create-videos-per-album'),
    path('videos/original/<int:session_album_id>/', get_original_videos, name='get_original_videos'),
    path('videos/watermarked/<int:session_album_id>/', get_watermarked_videos, name='get_watermarked_videos'),
    path('videos_by_seess/<int:session_album_id>/', get_videos_by_session, name='get_videos_by_session'),


    path('waves/<int:session_album_id>/', get_waves_for_session_album, name='waves-for-session-album'),
    path('api/get_waves/', get_waves, name='get_waves'),

    path('images/<int:wave_id>/', get_images_for_wave, name='images-for-wave'),

    path('api/get_images_for_multiple_waves/', get_images_for_multiple_waves, name='get_images_for_multiple_waves'),
    path('api/get_images_by_ids/', get_images_by_ids, name='get_images_by_ids'),
    path('api/get_videos_by_ids/', get_videos_by_ids, name='get_videos_by_ids'),

    path('watermarked_photos/<int:wave_id>/', get_watermarked_photos_by_wave, name='get_watermarked_photos_by_wave'),

    path("account_link/", create_account_link, name="create_account_link"),
    path("account/", create_account, name="create_account"),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    path('webhook/stripe/invoke_lambda', stripe_webhook_invoke_lambda, name='stripe-webhook-invoke-lambda'),
    path('api/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('create_account_session/', create_account_session, name='create_account_session'),
    path('create_account_session_for_alerts/', create_account_session_for_alerts, name='create_account_session_for_alerts'),
    path('test-webhook/', test_webhook_invoke_lambda, name='test-webhook'),

    path('invoke-lambda/', invoke_lambda_view, name='invoke_lambda'),

]