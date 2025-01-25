from django.urls import path
from .views import (
    product_detail, product_list, get_product_list_json, get_product_detail_json, delete_review, toggle_wishlist, wishlist_list
)

urlpatterns = [
    path("products/", product_list, name="product_list"),
    path("product/<uuid:pk>/", product_detail, name="product_detail"),
    path('reviews/<uuid:pk>/delete/', delete_review, name="delete_review"),
    path('toggle-wishlist/<uuid:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    
    # JSON Endpoints
    path('api/products/', get_product_list_json, name="api_product_list"),
    path('api/products/<uuid:pk>/', get_product_detail_json, name="api_product_detail"),
    path("wishlist/", wishlist_list, name="wishlist_list"),

]
