from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main.views import show_main, for_you_view


app_name = 'main'

urlpatterns = [
    # Publicly accessible main page
    path('', show_main, name='show_main'),
    path("for-you/", for_you_view, name="for_you"),
]