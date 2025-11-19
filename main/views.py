from datetime import datetime
import json, requests
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.utils.html import strip_tags

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.core.paginator import Paginator
from .models import Product
from .forms import ProductForm

logger = logging.getLogger(__name__)

# registration/login function

def register(request):
    if request.method == "POST":
        # AJAX/JSON
        if request.headers.get("Content-Type") == "application/json":
            try:
                data = json.loads(request.body)
                form = UserCreationForm(data)
                if form.is_valid():
                    form.save()
                    return JsonResponse({"success": True, "message": "Account created", "redirect": reverse("main:login")})
                else:
                    errors = []
                    for field, field_errors in form.errors.items():
                        for error in field_errors:
                            errors.append(f"{field}: {error}")
                    return JsonResponse({"success": False, "message": "Registration failed", "errors": errors}, status=400)
            except (json.JSONDecodeError, KeyError):
                return JsonResponse({"success": False, "message": "Invalid request data"}, status=400)
        
        # Traditional fallback
        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been successfully created!')
                return redirect('main:login')
    
    form = UserCreationForm()
    data = {'form': form}
    return render(request, 'register.html', data)

def login_user(request):
    if request.method == 'POST':
        # AJAX/JSON
        if request.headers.get("Content-Type") == "application/json":
            try:
                data = json.loads(request.body)
                username = data.get("username")
                password = data.get("password")

                if username and password:
                  user = authenticate(request, username=username, password=password)
                  if user is not None:
                    login(request, user)
                    response = JsonResponse({"success": True, "message": "Login successful", "redirect": reverse("main:show_main")})
                    response.set_cookie('last_login', str(datetime.now()))
                    return response

                return JsonResponse({"success": False, "message": "Invalid username or password"}, status=400)
            except (json.JSONDecodeError, KeyError):
                return JsonResponse({"success": False, "message": "Invalid request data"}, status=400)
        
        # Traditional fallback
        else:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                response = redirect("main:show_main")
                response.set_cookie('last_login', str(datetime.now()))
                return response
            else:
                form = AuthenticationForm(request)
        
        context = {'form': form}
        return render(request, 'login.html', context)
    
    else:
        form = AuthenticationForm(request)
        context = {'form': form}
        return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    response.set_cookie('toast', 'logout')
    return response

# flutter integration

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # Fetch image from external source
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        logger.exception(f"Error fetching image from URL: {image_url}")
        return HttpResponse('Error fetching image. Please try again later.', status=500)

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        # Assuming Flutter app handles session cookies for authentication
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Authentication required."}, status=401)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)

        name = data.get("name")
        price = data.get("price")
        descriptions = data.get("descriptions")
        category = data.get("category")
        
        if not all([name, price, descriptions, category]):
            return JsonResponse({"status": "error", "message": "Missing required fields: name, price, descriptions, category."}, status=400)

        try:
            price = int(price)
            if price <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return JsonResponse({"status": "error", "message": "Price must be a positive integer."}, status=400)

        valid_categories = [choice[0] for choice in Product.PRODUCT_OPTIONS]
        if category not in valid_categories:
            return JsonResponse({"status": "error", "message": f"Invalid category. Must be one of: {', '.join(valid_categories)}"}, status=400)

        product = Product.objects.create(
            user=request.user,
            name=strip_tags(name),
            price=price,
            descriptions=strip_tags(descriptions),
            category=category,
            thumbnail=data.get("thumbnail", ""),
            is_featured=data.get("is_featured", False)
        )

        return JsonResponse({"status": "success", "message": "Product created successfully.", "product_id": str(product.id)}, status=201)

    return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'all':
        product_list = Product.objects.all();
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'npm' : '2406434292',
        'name': 'Faiz Yusuf Ridwan',
        'class': 'PBP C',
        'product_list' : product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),

    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()
    data = {
        'product' : product
    }

    return render(request, "product_details.html", data)

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.user != product.user:
        return JsonResponse({"error": "You do not have permission to delete this product."}, status=403)
    if request.method == "POST":
        product.delete()
        return JsonResponse({"message": "deleted"}, status=200)

    return JsonResponse({"error": "Invalid method"}, status=405)

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.user != product.user:
        return JsonResponse({"error": "You do not have permission to edit this product."}, status=403)
    if request.method == "POST":
        if request.headers.get("Content-Type") == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)
        product.descriptions = data.get("descriptions", product.descriptions)
        product.thumbnail = data.get("thumbnail", product.thumbnail)
        product.category = data.get("category", product.category)
        product.save()

        return JsonResponse({"message": "updated"}, status=200)

    return JsonResponse({"error": "Invalid method"}, status=405)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_xml_by_id(request, product_id):
    try:
        product_list = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_list)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json(request):
    product_list = Product.objects.select_related('user').all().order_by('-date')
    
    paginator = Paginator(product_list, 20) # Show 20 products per page.
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    data = [
        {
            'id' : str(product.id),
            'user_id': product.user.id if product.user else None,
            'user_name': product.user.username if product.user else 'Anonymous',
            'name' : product.name,
            'price' : product.price,
            'descriptions' : product.descriptions,
            'date' : product.date.isoformat() if product.date else None,
            'item_views' : product.item_views,
            'thumbnail' : product.thumbnail,
            'category' : product.category,
            'is_featured' : product.is_featured,
            'is_product_trending': product.is_product_trending,
        }
        for product in page_obj
    ]
    
    response_data = {
        'total_results': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'results': data
    }
    return JsonResponse(response_data)

@login_required(login_url='/login')
def show_my_json(request):
    # This view returns JSON data for products belonging to the logged-in user.
    product_list = Product.objects.filter(user=request.user).order_by('-date')
    
    data = [
        {
            'id' : str(product.id),
            'user_id': product.user.id,
            'user_name': product.user.username,
            'name' : product.name,
            'price' : product.price,
            'descriptions' : product.descriptions,
            'date' : product.date.isoformat() if product.date else None,
            'item_views' : product.item_views,
            'thumbnail' : product.thumbnail,
            'category' : product.category,
            'is_featured' : product.is_featured,
            'is_product_trending': product.is_product_trending,
        }
        for product in product_list
    ]
    
    return JsonResponse(data, safe=False)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'user_id': product.user.id if product.user else None,
            'user_name': product.user.username if product.user else 'Anonymous',
            'name': product.name,
            'price': product.price,
            'descriptions': product.descriptions,
            'date': product.date.isoformat() if product.date else None,
            'item_views': product.item_views,
            'thumbnail': product.thumbnail or None,
            'category': product.category,
            'is_featured': product.is_featured,
            'is_product_trending': product.is_product_trending,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@require_POST
@login_required(login_url='/login')
def add_product_entry_ajax(request):
    if request.method == "POST":
        is_featured_val = False
        if request.headers.get("Content-Type") == "application/json":
            data = json.loads(request.body)
            is_featured_val = data.get("is_featured", False)
        else:
            data = request.POST
            # HTML forms send 'on' for checked boxes.
            if data.get("is_featured") == "on":
                is_featured_val = True

        product = Product.objects.create(
            user=request.user,
            name=data.get("name", ""),
            price=data.get("price", 0),
            descriptions=data.get("descriptions", ""),
            thumbnail=data.get("thumbnail", ""),
            category=data.get("category", ""),
            is_featured=is_featured_val,
        )

        return JsonResponse({"message": "Product added", "id": str(product.id)}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)
