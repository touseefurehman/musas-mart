from django.db import models
from ckeditor.fields import RichTextField

class GeneralSetting(models.Model):
    site_name = models.CharField(max_length=100, default="My Website")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    favicon = models.ImageField(upload_to='favicons/', null=True, blank=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    support_email = models.EmailField(blank=True, null=True)

    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)

    about_us = RichTextField(blank=True, null=True)
    privacy_policy = RichTextField(blank=True, null=True)
    terms_and_conditions = RichTextField(blank=True, null=True)
    refund_policy = RichTextField(blank=True, null=True)
    disclaimer = RichTextField(blank=True, null=True)

    footer_text = models.CharField(max_length=200, blank=True, null=True)
    copyright_text = models.CharField(max_length=200, blank=True)

    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    google_analytics_code = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Enforce only one instance
        self.pk = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "General Setting"
        verbose_name_plural = "General Setting"
        
        
        
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
  
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"