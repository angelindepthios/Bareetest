from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('my-page/', views.my_page, name='my_page'),
    path('get-user-reviews/', views.get_user_reviews, name='get_user_reviews'),
    path('wishlist-view/', views.wishlist_view, name='wishlist_view'),
]