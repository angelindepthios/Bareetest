from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main.views import show_main


app_name = 'main'

urlpatterns = [
    # Publicly accessible main page
    path('', show_main, name='show_main'),
]