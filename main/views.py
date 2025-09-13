from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .models import Product
from .forms import ProductForm

def show_main(request):
    product_list = Product.objects.all();

    context = {
        'npm' : '2406434292',
        'name': 'Faiz Yusuf Ridwan',
        'class': 'PBP C',
        'product_list' : product_list
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    data = {
        'form' : form 
    }
    return render(request,"add-product.html", data)

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()
    data = {
        'product' : product
    }

    return render(request, "product_details.html", data)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product.delete()
        return redirect('main:show_main')
    return render(request, "confirm_delete.html", {"product": product})

# show Data in formatted ways

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
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_json_by_id(request, product_id):
    try:
        product_list = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_list])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
       return HttpResponse(status=404)



# Create your views here.
