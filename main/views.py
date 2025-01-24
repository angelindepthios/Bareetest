from django.shortcuts import render

def show_main(request):
    context = {
        'login_user': request.user.username if request.user.is_authenticated else None,
        'last_login': request.COOKIES.get('last_login', 'No recent login'),
    }

    return render(request, "main.html", context)

