from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from .models import Product
from items.models import ItemCategory, CheckoutInfo
import cloudinary.uploader
import random



def upload_image_view(request):

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        result = cloudinary.uploader.upload(uploaded_file, public_id="test_image")
        return JsonResponse({'url': result['secure_url']})
    return JsonResponse({'error': 'No file uploaded'}, status=400)





# -------------------- Random Products --------------------
def random_products(request):
    query = request.GET.get('q', '')
    categories = ItemCategory.objects.all()

    products_qs = Product.objects.only('id', 'title', 'price', 'image')  # load minimal fields
    if query:
        products_qs = products_qs.filter(title__icontains=query)

    products = list(products_qs)
    random.shuffle(products)

    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'products': [{
                'id': p.id,
                'title': p.title,
                'price': p.price,
                'image_url': p.image.url if p.image else '',
            } for p in page_obj]
        })

    return render(request, 'random_products.html', {'page_obj': page_obj, 'categories': categories})



# def random_products(request):
#     query = request.GET.get('q', '')  # Get the search query
#     products = list(Product.objects.all())  # Get all products
#     random.shuffle(products)  # Shuffle the products
#     categories = ItemCategory.objects.all()

#     if query:
#         products = [product for product in products if query.lower() in product.title.lower()]

#     if not products:
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return JsonResponse({'products': []})  # Return empty JSON response for AJAX
#         return render(request, 'random_products.html', {'message': 'No products found.'})  # For normal page load

#     paginator = Paginator(products, 16)  # Paginate with 8 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if AJAX request
#         products_data = [
#             {
#                 'id': product.id,
#                 'title': product.title,
#                 'price': product.price,
#                 'image_url': product.image.url if product.image else '',
#             }
#             for product in page_obj
#         ]
#         return JsonResponse({'products': products_data})

#     return render(request, 'random_products.html', {'page_obj': page_obj,'categories': categories })



def track(request):
    order_info = None
    error_message = None

    if request.method == "GET" and "tracking_key" in request.GET:
        tracking_key = request.GET.get("tracking_key", "").strip()

        if tracking_key:
            try:
                order_info = CheckoutInfo.objects.get(tracking_key=tracking_key)
            except CheckoutInfo.DoesNotExist:
                error_message = "Invalid tracking key. No order found."
        else:
            error_message = "Please enter a tracking key."

    return render(request, "track.html", {"order_info": order_info, "error_message": error_message})

 # views for category of items
def Category (request):
    items_cate= ItemCategory.objects.all()
    return render(request,'search_pages/search.html',{'items_cat':items_cate})


# views for items of category
def test(request, id_cat=None):
    search_query = request.GET.get('q')

    if id_cat:
        Category_of_items = get_object_or_404(ItemCategory, id=id_cat)
        rental_items = Product.objects.filter(Category_of_items_id=id_cat)
        if search_query:
            rental_items = rental_items.filter(title__icontains=search_query)
    elif search_query:
        rental_items = Product.objects.filter(title__icontains=search_query).order_by('id')
    else:
        rental_items = Product.objects.all().order_by('id')

    paginator = Paginator(rental_items, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    if id_cat:
        context['category'] = Category_of_items

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, "search_pages/search_by_category.html", context)
    else:
        return render(request, "search_pages/search_by_category.html", context)

    
    
    
    
def my_item(request):
    user = request.user
    rental_items = Product.objects.filter(user=user)
    
    return render(request, 'items/my_item.html', {'rental_items': rental_items, 'user': user})







def pdp(request, id_cat, rental_item_id):
    product = get_object_or_404(Product, pk=rental_item_id)  # Rename variable
    category_of_items = get_object_or_404(ItemCategory, id=id_cat)
    all_products = Product.objects.exclude(id=product.id)
    random_products = random.sample(list(all_products), min(4, all_products.count()))
    
    return render(request, 'pdp.html', {
        'product': product,  # Use lowercase in context
        "category_of_items": category_of_items,
        'random_products': random_products
    })



def checkout(request, product_item_id):
    rental_item_instance = get_object_or_404(Product, id=product_item_id)
    category_of_items = rental_item_instance.Category_of_items  # Assuming there is a foreign key

    if request.method == "POST":
        username = request.POST.get("username")
        quantity_str = request.POST.get("quantity", "1")  # Get quantity as a string (default to "1")
        
        try:
            quantity = int(quantity_str)  # Convert to integer
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect('checkout', product_item_id=product_item_id)
        email = request.POST.get("Email")
        mobile_number = request.POST.get("Mobile_NUmber")  
        address = request.POST.get("address")
        country = request.POST.get("country")
        note_to_lender = request.POST.get("note_to_lender")


        if rental_item_instance.quantity < quantity:
            messages.error(request, f"Out of Stock! Only {rental_item_instance.quantity} items available.")
            return redirect('checkout', product_item_id=product_item_id)  # Redirect back to checkout page






        # Save the checkout information
        checkout_info = CheckoutInfo.objects.create(
            Category_of_items_checkout=category_of_items,  # Adjusted to match model field
            Product=rental_item_instance,  # Matches model field
            username=username,
            quantity=quantity,
            email=email,
            mobile_number=mobile_number,
            address=address,
            country=country,
            note_to_lender=note_to_lender,
        )


        messages.success(request, "Your order has been placed successfully! you will receive a call for oder conformation you also track your oder by using tracking key in track oder section. save this key.")
        return render(request, 'checkout.html', {
            'rental_item_instance': rental_item_instance,
            'tracking_key': checkout_info.tracking_key  # Pass tracking key to template
        })

    return render(request, 'checkout.html', {'rental_item_instance': rental_item_instance})








    
    
def privacy(request):

    return render(request, 'privacy.html')

    
    
def faq(request):

    return render(request, 'faq.html')
    
def term(request):

    return render(request, 'term.html')




from django.shortcuts import render
from .models import Product 

def searchs(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'query': query, 'results': results})