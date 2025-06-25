from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import GeneralSetting

@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow add only if no record exists
        return not GeneralSetting.objects.exists()

    def changelist_view(self, request, extra_context=None):
        try:
            setting = GeneralSetting.objects.get(pk=1)
            return HttpResponseRedirect(f'/admin/general/generalsetting/{setting.pk}/change/')
        except GeneralSetting.DoesNotExist:
            return HttpResponseRedirect(f'/admin/general/generalsetting/add/')

    fieldsets = (
        ('Basic Info', {'fields': ('site_name', 'logo', 'favicon')}),
        ('Contact Info', {'fields': ('phone', 'email', 'support_email', 'whatsapp_number', 'address')}),
        ('Social Media', {'fields': ('facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok')}),
        ('Content Pages', {'fields': ('about_us', 'privacy_policy', 'terms_and_conditions', 'refund_policy', 'disclaimer')}),
        ('Footer', {'fields': ('footer_text', 'copyright_text')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'google_analytics_code')}),
        ('Updated At', {'fields': ('updated_at',)}),
    )
    readonly_fields = ['updated_at']






from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')