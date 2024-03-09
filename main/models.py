import time
import string
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# USER MODEL DEFINITION
GENDER = (
    ('--Select Gender--', '--Select Gender--'),
    ('male', 'Male'),
    ('female', 'Female')
)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True "
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True"
            )

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    shop_description = models.TextField(
        max_length=1024, default="Welcome...", blank=True)
    shop_url = models.CharField(max_length=250, default="No link yet...", blank=True)
    num_ads = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=13, null=True)
    gender = models.CharField(max_length=200, choices=GENDER, null=True)
    state = models.CharField(max_length=200, default='Lagos' , blank=True)
    lga = models.CharField(max_length=200, default='Lagos Mainland', blank=True)
    
    #SOCIAL LINKS
    facebook = models.CharField(_("Facebook link"), max_length=200, null=True, default="No Facebook link provided", blank=True)
    x_twitter = models.CharField(_("X/Twitter link"), max_length=200, null=True, default="No X/Twitter link provided", blank=True)
    instagram = models.CharField(_("Instagram link"), max_length=200, null=True, default="No Instagram link provided", blank=True)
    linkedin = models.CharField(_("Linkedin link"), max_length=200, null=True, default="No LinkedIn link provided", blank=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username


'''END OF USER MODEL DEFINITION'''

'''Product models'''

CATEGORY = (
    ('Agriculture & Food', 'Agriculture & Food'),
    ('Babies & Kids', 'Babies & Kids'),
    ('Commercial equipment & Tools', 'Commercial equipment & Tools'),
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Electronics', 'Electronics'),
    ('Health & Beauty', 'Health & Beauty'),
    ('Home, Furniture & Appliances', 'Home, Furniture & Appliances'),
    ('Jobs', 'Jobs'),
    ('Mobile Phones & Tablets', 'Mobile Phones & Tablets'),
        ('Pets', 'Pets'),
    ('Hobbies, Sport and Fitness', 'Hobbies, Sport and Fitness'),
    ('Games', 'Games'),
    ('Services', 'Services'),
    ('Books', 'Books'),
    ('Movies and Music', 'Movies and Music'),
    ('Repair & Construction', 'Repair & Construction'),
    ('Sports, Arts & Outdoors', 'Sports, Arts & Outdoors'),
    ('Vehicles', 'Vehicles'),
)


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.CharField(max_length=1024, blank=True)
    product_image = models.ImageField(upload_to="images/", blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    category = models.CharField(max_length=150, default='N/A')
    sub_category = models.CharField(max_length=150, default='N/A')
    date_added = models.DateTimeField(auto_now_add=True)
    retailer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class CloudinaryURLs(models.Model):
    productt = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='cloudinaryurls_set')
    link = models.URLField(blank=True, max_length=1024)

    class Meta:
        verbose_name = _("Cloudinary URL")
        verbose_name_plural = _("Cloudinary URLs")

    def __str__(self):
        return self.link


'''END OF PRODUCT MODEL DEFINITION'''


class Review(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer} said "{self.comment}"'


class Reply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")

    def __str__(self):
        return f"{self.user} replied to {self.review.buyer}"


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    receipent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'{self.sender.username} to {self.receipent.username}'
    
    

class CartItem(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product}"


class Order(models.Model):
    order_code = models.CharField(max_length=9, unique=True, blank=True)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # product = models.ManyToManyField(Product)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"
