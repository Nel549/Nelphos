from django.contrib import admin
from .models import UserProfile, Cart, Library
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(Library)
