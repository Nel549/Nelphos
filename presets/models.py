from itertools import product
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Tags(models.Model):
    name = models.TextField(max_length=30)

    def __str__(self):
        return str(self.name)

class Preset(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500)
    file = models.FileField(upload_to='presets/files')
    cover = models.ImageField(upload_to = 'presets/covers', null = True, blank = True)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        validators=[MinValueValidator(0)]
    )
    tags = models.ManyToManyField(Tags)
    rateing = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Preset, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.product.name)



