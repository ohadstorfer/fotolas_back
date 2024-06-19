# serializers.py
from rest_framework import serializers
from .models import  AlbumsPrices, Chat, CustomUser, Message, Photographer, Spot, SessionAlbum, Img, SpotLike, Follower, Order, Wave
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['fullName'] = user.fullName
        token['id'] = user.id
        return token

    def validate(self, attrs):
            data = super().validate(attrs)

            # Add additional data to the response
            data['email'] = self.user.email
            data['fullName'] = self.user.fullName
            data['id'] = self.user.id

            return data



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'fullName', 'is_athlete', 'is_photographer', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
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
    class Meta:
        model = Spot
        fields = '__all__'

class SessionAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionAlbum
        fields = '__all__'

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



class WaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wave
        fields = ['id', 'session_album', 'cover_image']





class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['id', 'photo','WatermarkedPhoto', 'wave', 'price']


class WatermarkedImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['WatermarkedPhoto']


# class ImgByPersonalAlbumSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Img
#         fields = '__all__'







class SessionAlbumWithDetailsSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = SessionAlbum
        fields = '__all__'

    def get_photographer_profile_image(self, obj):
        if obj.photographer.profile_image:
            return obj.photographer.profile_image
        return None
    


class SessionAlbumByPhotographerSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.CharField(source='photographer.profile_image', read_only=True)

    class Meta:
        model = SessionAlbum
        fields = '__all__'


class SessionAlbumBySpotSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    photographer_name = serializers.ReadOnlyField(source='photographer.user.fullName')
    photographer_profile_image = serializers.CharField(source='photographer.profile_image', read_only=True)

    class Meta:
        model = SessionAlbum
        fields = '__all__'
    


