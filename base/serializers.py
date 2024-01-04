# serializers.py
from rest_framework import serializers
from .models import AlbumsPrices, Chat, CustomUser, Message, Photographer, Spot, SessionAlbum, PersonalAlbum, Img, CensoredImg, SpotLike, Follower, Order
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = '__all__'

class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = '__all__'

class SessionAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionAlbum
        fields = '__all__'

class PersonalAlbumSerializer(serializers.ModelSerializer):
    image_count = serializers.SerializerMethodField()

    def get_image_count(self, obj):
        return self.context['image_counts'][obj.id]

    class Meta:
        model = PersonalAlbum
        fields = '__all__'

class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = '__all__'

class CensoredImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = CensoredImg
        fields = '__all__'

class SpotLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotLike
        fields = '__all__'

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
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






class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.get_full_name()
        # Add more custom claims if needed
        return token

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'country', 'fullName', 'is_athlete', 'is_photographer']






class ImgByPersonalAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = '__all__'







class SessionAlbumWithDetailsSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = SessionAlbum
        fields = '__all__'

    def get_photographer_profile_image(self, obj):
        request = self.context.get('request', None)
        # Construct the complete URL by joining the server URL with the relative path
        if request and obj.photographer.profile_image:
            return request.build_absolute_uri(obj.photographer.profile_image.url)
        return None
    


class SessionAlbumByPhotographerSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = SessionAlbum
        fields = '__all__'

    def get_photographer_profile_image(self, obj):
        request = self.context.get('request', None)
        # Construct the complete URL by joining the server URL with the relative path
        if request and obj.photographer.profile_image:
            return request.build_absolute_uri(obj.photographer.profile_image.url)
        return None
    


class SessionAlbumBySpotSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = SessionAlbum
        fields = '__all__'

    def get_photographer_profile_image(self, obj):
        request = self.context.get('request', None)
        if request and obj.photographer.profile_image:
            return request.build_absolute_uri(obj.photographer.profile_image.url)
        return None