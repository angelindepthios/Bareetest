import datetime, pytz
from .forms import UserRegistForm, UserLoginForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def register_user(request):
    if request.method == 'POST':
        form = UserRegistForm(request.POST)
        if form.is_valid():
            form.save()
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