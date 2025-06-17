
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from items import urls
from general import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('items.urls'),name='list_an_item'),
    path('blog/', include('general.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
