from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.db.models import Count

class CustomUserManager(UserManager):
    def _create_user(self, email, password, fullName, is_athlete=True, is_photographer=False, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        if not password:
            raise ValueError("The password field must be provided")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            fullName=fullName,
            is_athlete=is_athlete,
            is_photographer=is_photographer,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None,  fullName=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be provided")
        if not password:
            raise ValueError("The password field must be provided")
        # Add additional validation if needed
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password,  fullName, **extra_fields)

    def create_superuser(self, email=None, password=None,  fullName=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be provided")
        if not password:
            raise ValueError("The password field must be provided")
        # Add additional validation if needed
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password,  fullName, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullName = models.CharField(max_length=255)
    is_athlete = models.BooleanField(default=True)
    is_photographer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    verification_status = models.CharField(max_length=255, blank=True, null=True)

    chats = models.ManyToManyField('Chat', related_name='user_chats', blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'fullName']

    def get_full_name(self):
        return self.fullName

    def get_short_name(self):
        return self.fullName or self.email.split('@')[0]



class Photographer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about = models.TextField()
    profile_image = models.CharField(default="default.png", max_length=255)
    cover_image = models.CharField(default="default.png", max_length=255)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user}'




class Spot(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255,null=True, blank=True)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.name}'


class SessionAlbum(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sessDate = models.DateTimeField()
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    cover_image = models.CharField(max_length=255, null=True, blank=True)
    videos = models.BooleanField(default=False)
    videosPerAlbums = models.BooleanField(default=False)
    forever = models.BooleanField(null=True, blank=True, default=True)
    dividedToWaves = models.BooleanField(null=True)
    active = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def set_expiration_date(self):
        if self.videos or self.videosPerAlbums:
            self.expiration_date = self.created_at + timedelta(days=30)
        else:
            self.expiration_date = self.created_at + timedelta(days=30)
        self.save()

    def is_active(self):
        if self.expiration_date and self.expiration_date < timezone.now():
            self.active = False
            self.save()
        return self.active





class Wave(models.Model):
    session_album = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE)
    cover_image = models.CharField(max_length=255, null=True, blank=True)

    def image_count(self):
        return self.img_set.count()
    


class Img(models.Model):
    photo = models.CharField(max_length=255, null=True, blank=True)
    WatermarkedPhoto = models.CharField(max_length=255, null=True, blank=True)
    wave = models.ForeignKey(Wave, on_delete=models.CASCADE, null=True,blank=True)
    SessionAlbum = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE, null=True, blank=True)



class Video(models.Model):
    video = models.CharField(max_length=255, null=True, blank=True)
    WatermarkedVideo = models.CharField(max_length=255, null=True, blank=True)
    wave = models.ForeignKey(Wave, on_delete=models.CASCADE, null=True,blank=True)
    SessionAlbum = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE, null=True, blank=True)
    img = models.CharField(max_length=255, null=True, blank=True)
    

class AlbumsPrices(models.Model):
    session_album = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE)
    price_1_to_5 = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    price_6_to_50 = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    price_51_plus = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)

    def __str__(self):
        return f'AlbumsPrices - Session Album: {self.session_album.id}'


class AlbumsPricesForVideos(models.Model):
    session_album = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE)
    price_1_to_3 = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    price_4_to_15 = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    price_16_plus = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)

    def __str__(self):
        return f'AlbumsPrices - Session Album: {self.session_album.id}'





class DefaultAlbumsPricesForImages(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    price_1_to_5 = models.DecimalField(max_digits=10, decimal_places=1, default=20.0)
    price_6_to_50 = models.DecimalField(max_digits=10, decimal_places=1, default=25.0)
    price_51_plus = models.DecimalField(max_digits=10, decimal_places=1, default=30.0)

    def __str__(self):
        return f'DefaultAlbumsPricesForImages - photographer: {self.photographer.id}'


class DefaultAlbumsPricesForVideos(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    price_1_to_3 = models.DecimalField(max_digits=10, decimal_places=1, default=20.0)
    price_4_to_15 = models.DecimalField(max_digits=10, decimal_places=1, default=25.0)
    price_16_plus = models.DecimalField(max_digits=10, decimal_places=1, default=30.0)

    def __str__(self):
        return f'DefaultAlbumsPricesForVideos - photographer: {self.photographer.id}'






class Purchase(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, related_name='purchases_as_photographer')
    surfer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='purchases_as_surfer', null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    netPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_item_quantity = models.IntegerField( null=True, blank=True)
    SessionAlbum = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE,null=True, blank=True)
    spot_name = models.CharField(max_length=255, null=True, blank=True)
    photographer_name = models.CharField(max_length=255, null=True, blank=True)
    surfer_name = models.CharField(max_length=255, null=True, blank=True)
    sessDate = models.DateTimeField(null=True)
    filenames = models.JSONField(null=True, blank=True)
    user_email = models.CharField(max_length=255, null=True, blank=True)
    zipFileName = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Purchase {self.id} - Photographer: {self.photographer_name}, Surfer: {self.surfer_name}'


class PurchaseItem(models.Model):
    PurchaseId = models.ForeignKey(Purchase , on_delete=models.CASCADE, related_name='order_items')
    Img = models.ForeignKey(Img, on_delete=models.CASCADE, related_name='Img', null=True, blank=True)
    Video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='Video', null=True, blank=True)
    





class SpotLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'spot')


class Follower(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'photographer')

class Message(models.Model):
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'{self.sender} to {self.receiver} at {self.timestamp}'


class Chat(models.Model):
    participants = models.ManyToManyField('CustomUser', related_name='user_chats')
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return ', '.join(str(user) for user in self.participants)
    



# 88888888888888888888888888888888888888888888888888   s3    88888888888888888888888888888888888888888888888888888888888888888888
    



def file_generate_upload_path(instance, filename):
	# Both filename and instance.file_name should have the same values
    return f"files/{instance.file_name}"


class File(models.Model):
    file = models.FileField(
        upload_to=file_generate_upload_path,
        blank=True,
        null=True
    )

    original_file_name = models.TextField()

    file_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=255)

    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        """
        We consider a file "valid" if the the datetime flag has value.
        """
        return bool(self.upload_finished_at)

    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == "s3":
            return self.file.url

        return f"{settings.APP_DOMAIN}{self.file.url}"