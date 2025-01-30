from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from products.models import Product
from blog.models import BlogPost
import random

def show_main(request):
    # Ambil 6 produk secara random
    all_products = list(Product.objects.all())
    random_products = random.sample(all_products, min(len(all_products), 6))

    # Ambil 6 blog secara random
    all_blogs = list(BlogPost.objects.all())
    random_blogs = random.sample(all_blogs, min(len(all_blogs), 6))

    return render(request, "main.html", {
        "random_products": random_products,
        "random_blogs": random_blogs
    })

@login_required
def for_you_view(request):
    user = request.user

    # Mapping skintype ke field database
    skintype_field = user.skintype.lower() if user.skintype else None

    # Function untuk mendapatkan 6 produk random sesuai skintype
    def get_random_skintype_products():
        if skintype_field:
            return Product.objects.filter(**{skintype_field: True}).order_by("?")[:6]
        return Product.objects.none()

    skintype_products = get_random_skintype_products()

    # Produk dengan rating tertinggi
    top_reviewed_products = (
        Product.objects.annotate(avg_rating=Avg("ratings__rating"))
        .order_by("-avg_rating")[:6]
    )

    # Blog dari authors dengan skintype yang sama
    blog_posts = BlogPost.objects.filter(author__skintype=user.skintype)[:6]

    context = {
        "skintype_products": skintype_products,
        "top_reviewed_products": top_reviewed_products,
        "blog_posts": blog_posts,
    }
    return render(request, "for_you.html", context)