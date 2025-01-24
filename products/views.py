from django.shortcuts import render
from django.conf import settings  # Import settings for BASE_DIR
from django.http import JsonResponse
import os
import json
from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Comment, Rating, Wishlist
from .forms import RatingCommentForm

def product_list(request):
    products = list(Product.objects.all())

    if not products:
        json_file_path = os.path.join(settings.BASE_DIR, "baree", "data", "dataset_uuid.json")

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                product_data = json.load(f)
                
                # Populate the database
                for item in product_data:
                    product, created = Product.objects.get_or_create(
                        id=item.get("pk"),  # Ensure the ID matches your model's field
                        defaults={
                            "id": item.get("pk"),
                            "label": item.get("label"),
                            "brand": item.get("brand"),
                            "name": item.get("name"),
                            "price": item.get("price"),
                            "ingredients": item.get("ingredients"),
                            "combination": item.get("combination"),
                            "dry": item.get("dry"),
                            "normal": item.get("normal"),
                            "oily": item.get("oily"),
                            "sensitive": item.get("sensitive"),
                        }
                    )
                products = list(Product.objects.all())
        else:
            products = []

    return render(request, "product_list.html", {"products": products})


def get_product_list_json(request):    
    products = list(Product.objects.all())

    if not products:
        json_file_path = os.path.join(settings.BASE_DIR, "baree", "data", "dataset_uuid.json")
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                products = json.load(f)
        else:
            products = []

    return JsonResponse(products, safe=False)

def product_detail(request, pk):
    try:
        # Attempt to fetch from the database
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        # Fallback to JSON file if the product isn't in the database
        json_file_path = os.path.join(settings.BASE_DIR, "baree", "data", "dataset_uuid.json")

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                products = json.load(f)

                # Safely find the product using "pk" instead of "id"
                product_data = next((p["fields"] for p in products if str(p.get("pk")) == str(pk)), None)

                if product_data:
                    return render(request, "product_detail.html", {"product": product_data})
        
        # Return 404 if not found in both the database and JSON
        return render(request, "404.html", status=404)

    return render(request, "product_detail.html", {"product": product})