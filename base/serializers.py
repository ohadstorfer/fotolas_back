# serializers.py
from django.forms import ValidationError
from rest_framework import serializers
from .models import  AlbumsPrices, AlbumsPricesForVideos, Chat, CustomUser, Message, Photographer,DefaultAlbumsPricesForImages, DefaultAlbumsPricesForVideos, Purchase, PurchaseItem, Spot, SessionAlbum, Img, SpotLike, Follower, Video, Wave
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, force_str
from rest_framework_simplejwt.tokens import UntypedToken



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['fullName'] = user.fullName
        token['id'] = user.id
        token['is_photographer'] = user.is_photographer
        return token

    def validate(self, attrs):
            data = super().validate(attrs)

            # Add additional data to the response
            data['email'] = self.user.email
            data['fullName'] = self.user.fullName
            data['id'] = self.user.id
            data['is_photographer'] = self.user.is_photographer

            return data



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email.")
        return value
    


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            UntypedToken(value)
        except:
            raise serializers.ValidationError("Invalid or expired token.")
        return value

    def validate(self, data):
        token = data['token']
        try:
            decoded_token = UntypedToken(token)
            user_id = decoded_token['user_id']
        except:
            raise serializers.ValidationError("Invalid or expired token.")

        data['user'] = CustomUser.objects.get(id=user_id)
        return data

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()





class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'fullName', 'is_athlete', 'is_photographer', 'password', 'stripe_account_id']

    def create(self, validated_data):
        # Convert the email to lowercase
        email = validated_data['email'].lower()

        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError( "A user with this email already exists.")

        # Create the user with the lowercase email
        user = CustomUser.objects.create(
            email=email,
            fullName=validated_data['fullName'],
            is_athlete=validated_data.get('is_athlete', False),
            is_photographer=validated_data.get('is_photographer', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user




class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = '__all__'



class SpotSerializer(serializers.ModelSerializer):
    session_album_count = serializers.SerializerMethodField()

    class Meta:
        model = Spot
        fields = '__all__'  # or specify the fields you want to include

    def get_session_album_count(self, obj):
        return SessionAlbum.objects.filter(spot=obj).count()
    



class SessionAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionAlbum
        fields = '__all__'



class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['id', 'photo', 'personal_album', 'price']

# class CensoredImgSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CensoredImg
#         fields = '__all__'

class SpotLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotLike
        fields = '__all__'

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = '__all__'

class AlbumsPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumsPrices
        fields = '__all__'

class AlbumsPricesForVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumsPricesForVideos
        fields = '__all__'

class DefaultAlbumsPricesForImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAlbumsPricesForImages
        fields = '__all__'  # You can specify fields here if you want

class DefaultAlbumsPricesForVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAlbumsPricesForVideos
        fields = '__all__'  # You can specify fields here if you want

class WaveSerializer(serializers.ModelSerializer):
    image_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Wave
        fields = ['id', 'session_album', 'cover_image', 'image_count']

# class PersonalAlbumSerializer(serializers.ModelSerializer):
#     image_count = serializers.SerializerMethodField()

#     def get_image_count(self, obj):
#         return self.context['image_counts'][obj.id]

#     class Meta:
#         model = PersonalAlbum
#         fields = '__all__'


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['id', 'photo','WatermarkedPhoto', 'wave', 'SessionAlbum']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

        

class WatermarkedImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['WatermarkedPhoto']


# class ImgByPersonalAlbumSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Img
#         fields = '__all__'




from django.utils import timezone
from datetime import timedelta


class SessionAlbumWithDetailsSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.SerializerMethodField()
    days_until_expiration = serializers.SerializerMethodField()
    photographer_stripe_account_id = serializers.ReadOnlyField(source='photographer.stripe_account_id')

    class Meta:
        model = SessionAlbum
        fields = '__all__'

    def get_photographer_profile_image(self, obj):
        if obj.photographer.profile_image:
            return obj.photographer.profile_image
        return None

    def get_days_until_expiration(self, obj):
        if obj.created_at:
            # Determine expiration duration based on whether it's videos or not
            if obj.videos:
                expiration_duration = timedelta(days=5)
            else:
                expiration_duration = timedelta(days=30)
            expiration_date = obj.created_at + expiration_duration
            remaining_time = expiration_date - timezone.now()
            # Return remaining days, ensuring it's not negative
            return max(0, remaining_time.days)
        return None
    


class SessionAlbumByPhotographerSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.CharField(source='photographer.profile_image', read_only=True)
    days_until_expiration = serializers.SerializerMethodField()

    class Meta:
        model = SessionAlbum
        fields = '__all__'


    def get_days_until_expiration(self, obj):
        if obj.expiration_date:
            remaining_time = obj.expiration_date - timezone.now()
            return max(0, remaining_time.days)  # Ensure non-negative value
        return None


class SessionAlbumBySpotSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.CharField(source='photographer.profile_image', read_only=True)
    days_until_expiration = serializers.SerializerMethodField()

    class Meta:
        model = SessionAlbum
        fields = '__all__'


    def get_days_until_expiration(self, obj):
        if obj.expiration_date:
            remaining_time = obj.expiration_date - timezone.now()
            return max(0, remaining_time.days)  # Ensure non-negative value
        return None
    