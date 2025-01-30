import datetime, pytz
from .forms import UserRegistForm, UserLoginForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from blog.models import BlogPost
from products.models import Product, RatingComment, Wishlist

def register_user(request):
    if request.method == 'POST':
        form = UserRegistForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.profile_photo = request.FILES.get('profile_photo')
            user.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    else:
        form = UserRegistForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Convert UTC time to local timezone (e.g., 'Asia/Jakarta')
            local_tz = pytz.timezone('Asia/Jakarta')
            local_time = datetime.datetime.now().astimezone(local_tz)

            # Redirect to the last visited page
            next_url = request.GET.get('next') or request.POST.get('next') or 'product_list'
            response = redirect(next_url)

            # Store the correct timezone-based datetime in cookie
            response.set_cookie('last_login', str(local_time.strftime('%Y-%m-%d %H:%M:%S %Z')))

            return response

        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    context = {'form': form, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = redirect('main:show_main')
    response.delete_cookie('last_login')
    return response

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Verifikasi password lama
        if not check_password(old_password, user.password):
            messages.error(request, 'Incorrect current password.', extra_tags='error')
            return redirect('change_password')

        # Validasi password baru
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.', extra_tags='error')
            return redirect('change_password')

        # Ubah password dan update session
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully!', extra_tags='success')
        return redirect('change_password')
    
    return render(request, 'change_password.html')

@login_required(login_url='/login/')
def get_user_reviews(request):
    """Fetch all reviews submitted by the logged-in user."""
    reviews = RatingComment.objects.filter(user=request.user).order_by("-timestamp")

    reviews_data = [
        {
            "product_id": review.product.id,
            "product_name": review.product.name,
            "rating": review.rating,
            "comment": review.comment,
            "timestamp": review.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for review in reviews
    ]

    return JsonResponse({"user_reviews": reviews_data})

@login_required
def my_page(request):
    # Get the user profile based on username
    user = request.user

    # Retrieve the user's blog posts and reviews
    blogs = BlogPost.objects.filter(author=user).order_by('-created_at')
    reviews = RatingComment.objects.filter(user=user).order_by('-timestamp')


    context = {
        'user': user,
        'blogs': blogs,
        'reviews': reviews,
    }
    return render(request, 'my_page.html', context) 

@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user) 
    
    context = {
        "wishlist_items": wishlist_items,
    }
    return render(request, "wishlist.html", context)
