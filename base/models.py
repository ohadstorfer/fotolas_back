from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.db.models import Count

class CustomUserManager(UserManager):
    def _create_user(self, email, password, country, fullName, is_athlete=True, is_photographer=False, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            country=country,
            fullName=fullName,
            is_athlete=is_athlete,
            is_photographer=is_photographer,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, country=None, fullName=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be provided")
        # Add additional validation if needed
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, country, fullName, **extra_fields)

    def create_superuser(self, email=None, password=None, country=None, fullName=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be provided")
        # Add additional validation if needed
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, country, fullName, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=255)
    fullName = models.CharField(max_length=255)
    is_athlete = models.BooleanField(default=True)
    is_photographer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    chats = models.ManyToManyField('Chat', related_name='user_chats', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['country', 'fullName']

    def get_full_name(self):
        return self.fullName

    def get_short_name(self):
        return self.fullName or self.email.split('@')[0]



class Photographer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about = models.TextField()
    profile_image = models.ImageField(default="default.png", null=True, blank=True)
    cover_image = models.ImageField(default="default.png" , null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user}'

class Spot(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.name}'


class SessionAlbum(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sessDate = models.DateTimeField(default=timezone.now)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    cover_image = models.ImageField(default="default.png")
    albums_prices = models.OneToOneField('AlbumsPrices', on_delete=models.CASCADE, null=True, blank=True)


class PersonalAlbum(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    session_album = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE)
    cover_image = models.ImageField(default="default.png")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def get_image_count(self):
        return Img.objects.filter(personal_album=self).count()

class Img(models.Model):
    photo = models.ImageField(default="default.png")
    personal_album = models.ForeignKey(PersonalAlbum, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class AlbumsPrices(models.Model):
    session_album = models.ForeignKey(SessionAlbum, on_delete=models.CASCADE)
    singlePhotoPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_1_to_5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_6_to_10 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_11_to_20 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_21_to_50 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_51_plus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'AlbumsPrices - Session Album: {self.session_album.id}'


class Order(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Order {self.id} - {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    personal_album = models.ForeignKey('PersonalAlbum', on_delete=models.CASCADE, null=True, blank=True)
    img = models.ForeignKey('Img', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Order Item {self.id} - {self.order.user}'



class CensoredImg(models.Model):
    img = models.ForeignKey(Img, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png")
    personal_album = models.ForeignKey(PersonalAlbum, on_delete=models.CASCADE)


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