from django.db import models
from django.db import models, transaction
import uuid
import os
from multiselectfield import MultiSelectField
from cloudinary.models import CloudinaryField
# Create your models here.
from django.db import models

class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    background_image = CloudinaryField('image/')

    def __str__(self):
        return self.title
    
    
    
    
# blog/models.py
from django.db import models
from django.utils.text import slugify

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
