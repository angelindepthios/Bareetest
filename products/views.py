from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Product, RatingComment, Wishlist
from .forms import RatingCommentForm
import os
import json
from django.conf import settings
from django.db.models import Q

def product_list(request):
    """Display all products, initialize database if empty, and allow searching & filtering."""
    products = Product.objects.all()

    # Initialize database if empty
    if not products.exists():
        json_file_path = os.path.join(settings.BASE_DIR, "baree", "data", "dataset_uuid.json")

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                product_data = json.load(f)

                for item in product_data:
                    Product.objects.get_or_create(
                        id=item.get("pk"),
                        defaults=item["fields"]
                    )
                    
            products = Product.objects.all()

    # Search Query
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(brand__icontains=query) | 
            Q(label__icontains=query)
        )

    # Filters
    brand = request.GET.get('brand', '').strip()
    label = request.GET.get('label', '').strip()
    skintype = request.GET.get('skintype', '')  # Avoid NoneType error
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    min_rating = request.GET.get('min_rating', '').strip()

    if brand:
        products = products.filter(brand__icontains=brand)

    if label:
        products = products.filter(label__icontains=label)

    if skintype.lower() in ["dry", "normal", "oily", "combination", "sensitive"]:
        filter_kwargs = {skintype.lower(): True}
        products = products.filter(**filter_kwargs)

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if min_rating:
        products = products.filter(rating__gte=min_rating)
        
    unique_brands = Product.objects.values_list('brand', flat=True).distinct()
    unique_labels = Product.objects.values_list('label', flat=True).distinct()

    context = {
        "products": products,
        "unique_brands": unique_brands,
        "unique_labels": unique_labels,
        "selected_brand": brand,
        "selected_label": label,
        "selected_skintype": skintype,
        "min_price": min_price,
        "max_price": max_price,
        "min_rating": min_rating
    }

    return render(request, "product_list.html", context)

def product_detail(request, pk):
    """Display product details, ratings, and comment submission form."""
    product = get_object_or_404(Product, pk=pk)
    form = RatingCommentForm()

    user_choices = []
    if request.user.is_authenticated:
        user_choices = Wishlist.objects.filter(user=request.user).values_list('product__pk', flat=True)

    if request.method == "POST":
        form = RatingCommentForm(request.POST)
        if form.is_valid():
            rating_comment = form.save(commit=False)
            rating_comment.product = product
            rating_comment.user = request.user
            rating_comment.save()
            return redirect('product_detail', pk=pk)

    return render(request, "product_detail.html", {
        "product": product,
        "form": form,
        "reviews": product.ratings.order_by("-timestamp"),
        "user_choices": user_choices,
    })


@login_required(login_url='/login/')
@csrf_exempt
def submit_review(request, pk):
    """Handle form submission for ratings & comments."""
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = RatingCommentForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return JsonResponse({
                "message": "Review submitted successfully!",
                "username": request.user.username,
                "rating": review.rating,
                "comment": review.comment,
                "timestamp": review.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }, status=201)
        return JsonResponse({"errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid submission"}, status=400)

def get_product_list_json(request):
    """Return all products in JSON format."""
    products = list(Product.objects.values())
    return JsonResponse(products, safe=False)

def get_product_detail_json(request, pk):
    """Return details & reviews for a specific product in JSON."""
    product = get_object_or_404(Product, pk=pk)
    data = {
        "id": str(product.id),
        "label": product.label,
        "brand": product.brand,
        "name": product.name,
        "price": float(product.price),
        "ingredients": product.ingredients,
        "average_rating": product.average_rating(),
        "reviews": list(product.ratings.values("rating", "comment", "user__username", "timestamp")),
    }
    return JsonResponse(data)

@login_required
def delete_review(request, pk):
    """Delete a review if the user is the author."""
    review = get_object_or_404(RatingComment, pk=pk)

    if review.user == request.user:
        review.delete()
    return redirect("product_detail", pk=review.product.pk)

@login_required(login_url='/login/')
def toggle_wishlist(request, product_id):
    if request.method == "POST":
        user = request.user
        product = get_object_or_404(Product, pk=product_id)

        # Check if the product is already in the wishlist
        wishlist_entry = Wishlist.objects.filter(user=user, product=product).first()

        if wishlist_entry:  # If it exists, remove it (toggle off)
            wishlist_entry.delete()
            return JsonResponse({"in_wishlist": False})
        else:  # If it does not exist, create it (toggle on)
            Wishlist.objects.create(user=user, product=product)
            return JsonResponse({"in_wishlist": True})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def wishlist_list(request):
    """Return a JSON response with the user's wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    
    data = [
        {
            "id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "added_at": item.added_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for item in wishlist_items
    ]

    return JsonResponse({"wishlist": data}, safe=False)

def get_reviews(request, pk):
    """Fetch all reviews for a product."""
    product = Product.objects.get(pk=pk)
    reviews = RatingComment.objects.filter(product=product).order_by("-timestamp")

    reviews_data = [
        {
            "username": review.user.username,
            "skintype" : review.user.skintype,
            "rating": review.rating,
            "comment": review.comment,
            "timestamp": review.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for review in reviews
    ]

    return JsonResponse({"reviews": reviews_data})