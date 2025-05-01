from django.db import models, transaction
import uuid
import os
from multiselectfield import MultiSelectField


class ItemCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_of_item/', blank=True, null=True)        

    def __str__(self):
        return self.name
















class Product(models.Model):   
    
    
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    Category_of_items = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="Category", null=True)
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()
    
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='M')  # ✅ Add this line

    description = models.TextField(max_length=200000000)
    image = models.ImageField(upload_to='Product_Image/', blank=True, null=True) 
    image2 = models.ImageField(upload_to='Product_Image/', blank=True, null=True)    
    image3 = models.ImageField(upload_to='Product_Image/', blank=True, null=True)        

    def __str__(self):
        return self.title























import uuid
from django.db import models, transaction

class CheckoutInfo(models.Model):
    STATUS_CHOICES = [
        ('storage', 'At Storage'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    Category_of_items_checkout = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="Category_item_checkout", null=True)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="checkout", null=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    address = models.TextField()
    country = models.CharField(max_length=100)
    note_to_lender = models.TextField()
    quantity = models.IntegerField(default=1)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='storage')
    admin_note = models.TextField(blank=True, null=True)  # Admin's note for buyer
    tracking_key = models.CharField(max_length=20, unique=True, editable=False)  # Tracking ID

    def save(self, *args, **kwargs):
        """ Restrict status changes and reduce product quantity when an order is placed """

        if not self.tracking_key:  # Generate only if not set
            self.tracking_key = str(uuid.uuid4())[:12]  # Generate a 12-character unique key

        if self.pk:  # If object already exists (update case)
            old_instance = CheckoutInfo.objects.get(pk=self.pk)

            # Prevent changing status after it is delivered or canceled
            if old_instance.status in ['delivered', 'canceled'] and self.status != old_instance.status:
                raise ValueError("Status cannot be changed after the order is delivered or canceled.")

            # Prevent changing from 'storage' to anything other than 'shipping'
            if old_instance.status == 'storage' and self.status not in ['storage', 'shipping']:
                raise ValueError("You can only change status from 'storage' to 'shipping'.")

            # Prevent changing from 'shipping' back to 'storage'
            if old_instance.status == 'shipping' and self.status == 'storage':
                raise ValueError("Cannot change status back to 'storage' after shipping.")

            # Prevent changing from 'canceled' to any other status
            if old_instance.status == 'canceled' and self.status != 'canceled':
                raise ValueError("Canceled orders cannot be changed.")

        if self.Product and not self.pk:  # Only deduct stock on first save (new order)
            with transaction.atomic():  # Ensure atomicity (all or nothing)
                product = Product.objects.select_for_update().get(id=self.Product.id)  # Lock row for update

                self.quantity = int(self.quantity)  # Ensure quantity is an integer
                
                if product.quantity < self.quantity:
                    raise ValueError("Not enough stock available.")  # Prevent saving if not enough stock
                
                product.quantity -= self.quantity  # Deduct purchased quantity
                product.save(update_fields=['quantity'])  # Save only the quantity field

        super().save(*args, **kwargs)

        
        
        
        
        
        
        def save(self, *args, **kwargs):
            """ Restrict status updates if already delivered """
            if self.pk:  # If object exists in the database
                existing_order = CheckoutInfo.objects.get(pk=self.pk)
                if existing_order.status == "delivered" and self.status != "delivered":
                    raise ValueError("Cannot change status after delivery.")
    def __str__(self):
        return self.username
