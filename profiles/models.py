from django.db import models
from django.conf import settings
from presets.models import Preset
from django.core.validators import MinValueValidator

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, null=True, blank=True)
    profileImage = models.ImageField(null=True, blank=True, upload_to = 'profile/images')
    instagram_link = models.CharField(null = True, blank=True, max_length=100)
    facebook_link = models.CharField(null = True, blank=True, max_length=100)
    tiktok_link = models.CharField(null = True, blank=True, max_length=100)
    twitter_link = models.CharField(null = True, blank=True, max_length=100)
    pinterest_link = models.CharField(null = True, blank=True, max_length=100)
    
    #class Meta:
        #unique_together = ('user', 'bio')

    def __str__(self):
        return str(self.user)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Preset, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Library(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Preset, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

