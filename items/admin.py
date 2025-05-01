from django.contrib import admin, messages
from django.utils.html import mark_safe
from django.utils.timezone import now
from .models import Product, ItemCategory, CheckoutInfo
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources
import uuid
import matplotlib.pyplot as plt
import io
import urllib
import base64
from django.db.models import Count

# ---------------- Resources ----------------
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ItemCategoryResource(resources.ModelResource):
    class Meta:
        model = ItemCategory

class CheckoutInfoResource(resources.ModelResource):
    class Meta:
        model = CheckoutInfo

# ---------------- Admins ----------------
class ItemCategoryAdmin(ImportExportModelAdmin):
    resource_class = ItemCategoryResource
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"

    image_preview.short_description = "Image Preview"

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('title', 'price', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"

    image_preview.short_description = "Image Preview"

class CheckoutInfoAdmin(ImportExportModelAdmin):
    resource_class = CheckoutInfoResource
    list_display = ('username', 'Product', 'status', 'tracking_key', 'admin_note')
    list_filter = ('status',)
    search_fields = ('username', 'email', 'mobile_number', 'tracking_key')
    readonly_fields = ('tracking_key', 'note_to_lender', 'username', 'email', 'mobile_number')
    fields = ('username', 'email', 'mobile_number', 'address', 'country', 'Product', 'status', 'tracking_key', 'note_to_lender', 'admin_note')
    actions = ['mark_as_shipped', 'mark_as_delivered']

    @admin.action(description="Mark selected as Shipping")
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipping')

    @admin.action(description="Mark selected as Delivered")
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')

    def save_model(self, request, obj, form, change):
        if change:
            old_instance = CheckoutInfo.objects.get(pk=obj.pk)
            if old_instance.status in ['delivered', 'canceled'] and obj.status != old_instance.status:
                messages.error(request, "❌ Status cannot be changed after the order is delivered or canceled.")
                return
            if old_instance.status == 'storage' and obj.status not in ['storage', 'shipping']:
                messages.error(request, "❌ You can only change status from 'storage' to 'shipping'.")
                return
            if old_instance.status == 'shipping' and obj.status == 'storage':
                messages.error(request, "❌ Cannot change status back to 'storage' after shipping.")
                return

        if not obj.tracking_key:
            obj.tracking_key = str(uuid.uuid4())[:12]
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        sales_data = (
            CheckoutInfo.objects.filter(status='delivered')
            .values('Product__title')
            .annotate(total_sold=Count('id'))
            .order_by('-total_sold')
        )

        if sales_data:
            product_names = [item['Product__title'] for item in sales_data]
            sales_counts = [item['total_sold'] for item in sales_data]

            plt.figure(figsize=(8, 4))
            plt.bar(product_names, sales_counts, color='blue')
            plt.xlabel("Product")
            plt.ylabel("Total Sales")
            plt.title("Sales Report")
            plt.xticks(rotation=45)

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graph_image = base64.b64encode(image_png).decode("utf-8")
            graph_url = f'data:image/png;base64,{graph_image}'

            plt.clf()
            plt.close()

            extra_context = extra_context or {}
            extra_context["sales_graph"] = mark_safe(f'<img src="{graph_url}" style="width: 100%;" />')

        return super().changelist_view(request, extra_context=extra_context)

# ---------------- Register Models ----------------
admin.site.register(Product, ProductAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(CheckoutInfo, CheckoutInfoAdmin)
