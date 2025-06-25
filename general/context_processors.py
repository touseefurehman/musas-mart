from .models import GeneralSetting

def general_settings(request):
    try:
        settings = GeneralSetting.objects.first()
    except GeneralSetting.DoesNotExist:
        settings = None
    return {
        'site_settings': settings
    }
