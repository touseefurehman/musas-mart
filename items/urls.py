from django.urls import path, include
from items import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
path('search_by_category/<int:id_cat>',views.test, name="search_by_category"),
path('my_item', views.my_item, name='my_item'), 
path('Home', views.Category, name='Category'),
path('', views.random_products, name='random_products'),
path('track', views.track, name='track'),

path('checkout/<int:product_item_id>/', views.checkout, name='checkout'),
path('pdp/<int:id_cat>/<int:rental_item_id>', views.pdp, name='pdp'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
