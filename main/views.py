from datetime import datetime
import json

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
from .models import Product
from .forms import ProductForm

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

@csrf_exempt
def create_product(request):
    product = get_object_or_404(Product, pk=id, user=request.user)
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
        return JsonResponse({"message": "Product updated"}, status=200)

    # If not AJAX POST fallback:
    return render(request, "edit_product.html", {"form": ProductForm(instance=product)})

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()
    data = {
        'product' : product
    }

    return render(request, "product_details.html", data)

@csrf_exempt
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product.delete()
        return JsonResponse({"message": "deleted"}, status=200)

    return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
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
    product_list = Product.objects.all()
    data = [
        {
            'id' : str(product.id),
            'user': product.user.username if product.user else None,
            'user_id': product.user.id if product.user else None,
            'name' : product.name,
            'price' : product.price,
            'descriptions' : product.descriptions,
            'date' : product.date,
            'item_views' : product.item_views,
            'thumbnail' : product.thumbnail,
            'category' : product.category,
            'is_featured' : product.is_featured,
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
            'user_name': product.user.username if product.user else 'Anonymous',  # For seller
            'name': product.name,  # ADDED: Missing name field
            'price': product.price,
            'descriptions': product.descriptions,
            'date': product.date.isoformat() if product.date else None,
            'item_views': product.item_views,
            'thumbnail': product.thumbnail or None,
            'category': product.category,
            'is_featured': product.is_featured,
            'is_product_trending': product.is_product_trending,  # ADDED: Serialized property
        }
        return JsonResponse(data, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Product not found'}, status=404)

@csrf_exempt
@require_POST

def add_product_entry_ajax(request):
    if request.method == "POST":
        if request.headers.get("Content-Type") == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        product = Product.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=data.get("name", ""),
            price=data.get("price", 0),
            descriptions=data.get("descriptions", ""),
            thumbnail=data.get("thumbnail", ""),
            category=data.get("category", ""),
            is_featured=data.get("is_featured", False),
        )

        return JsonResponse({"message": "Product added", "id": str(product.id)}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)

