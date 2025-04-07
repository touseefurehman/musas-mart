from django.contrib import admin,messages
from django.utils.html import mark_safe
from .models import Product, ItemCategory, CheckoutInfo
from django.utils.timezone import now
from django.core.exceptions import ValidationError




from django.utils.safestring import mark_safe
import matplotlib.pyplot as plt
import io
import urllib
import base64
from .models import CheckoutInfo
from django.db.models import Count
from django.utils.timezone import now

class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')  # Show name and image preview

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"

    image_preview.short_description = "Image Preview"  # Change column name in admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"

    image_preview.short_description = "Image Preview"

admin.site.register(Product, ProductAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)


class CheckoutInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'Product', 'status', 'tracking_key', 'admin_note')  # Show these fields in the list
    list_filter = ('status',)  # Add a filter by status
    search_fields = ('username', 'email', 'mobile_number', 'tracking_key')  # Enable search
    readonly_fields = ('tracking_key', 'note_to_lender','username', 'email', 'mobile_number')  # Prevent editing of these fields
    fields = ('username',  'email', 'mobile_number', 'address', 'country', 'Product', 'status', 'tracking_key', 'note_to_lender', 'admin_note')  # Ensure "Note to Lender" is visible

    actions = ['mark_as_shipped', 'mark_as_delivered']  # Custom admin actions


    @admin.display(ordering='status', description="Status Grouping")
    def grouped_status(self, obj):
        """ Custom display to highlight status groups """
        status_colors = {
            'pending': 'gray',
            'shipping': 'blue',
            'delivered': 'green',
            'canceled': 'red',
            'storage': 'orange'
        }
        color = status_colors.get(obj.status, 'black')
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{obj.status}</span>')


    def save_model(self, request, obj, form, change):
        if not obj.tracking_key:
            obj.tracking_key = str(uuid.uuid4())[:12]  # Generate tracking key
        super().save_model(request, obj, form, change)

    # Custom actions for bulk updating status
    @admin.action(description="Mark selected as Shipping")
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipping')

    @admin.action(description="Mark selected as Delivered")
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')

    list_display = ('username', 'Product', 'status', 'tracking_key')
    actions = None  # Disable bulk actions if necessary

    def save_model(self, request, obj, form, change):
        """ Show an error message instead of crashing """
        if change:  # If updating an existing record
            old_instance = CheckoutInfo.objects.get(pk=obj.pk)

            if old_instance.status in ['delivered', 'canceled'] and obj.status != old_instance.status:
                messages.error(request, "❌ Status cannot be changed after the order is delivered or canceled.")
                return  # Prevent saving

            if old_instance.status == 'storage' and obj.status not in ['storage', 'shipping']:
                messages.error(request, "❌ You can only change status from 'storage' to 'shipping'.")
                return  # Prevent saving

            if old_instance.status == 'shipping' and obj.status == 'storage':
                messages.error(request, "❌ Cannot change status back to 'storage' after shipping.")
                return  # Prevent saving

        super().save_model(request, obj, form, change)  # Save if no issues
        
        
        
        
        
        
        
        
        
        
        
        
    class CheckoutInfoAdmin(admin.ModelAdmin):
     list_display = ('username', 'Product', 'status', 'tracking_key')

    def changelist_view(self, request, extra_context=None):
        """ Add a sales graph in Django Admin """
        # Aggregate sales data
        sales_data = (
            CheckoutInfo.objects.filter(status='delivered')  # Only delivered orders count as sales
            .values('Product__title')  # Corrected the query
            .annotate(total_sold=Count('id'))  # Count number of sales per product
            .order_by('-total_sold')  # Sort by highest sales
        )

        if sales_data:
            product_names = [item['Product__title'] for item in sales_data]  # Extract product names
            sales_counts = [item['total_sold'] for item in sales_data]  # Extract sales numbers

            # Create a bar chart
            plt.figure(figsize=(8, 4))
            plt.bar(product_names, sales_counts, color='blue')
            plt.xlabel("Product")
            plt.ylabel("Total Sales")
            plt.title("Sales Report")
            plt.xticks(rotation=45)

            # Convert the graph into an image
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            # Convert image to base64
            graph_image = base64.b64encode(image_png).decode("utf-8")
            graph_url = f'data:image/png;base64,{graph_image}'

            # Cleanup to prevent memory issues
            plt.clf()
            plt.close()

            # Add graph to the admin panel
            extra_context = extra_context or {}
            extra_context["sales_graph"] = mark_safe(f'<img src="{graph_url}" style="width: 100%;" />')

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(CheckoutInfo, CheckoutInfoAdmin)

