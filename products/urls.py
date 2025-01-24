from django.urls import path
from .views import (
    product_detail, product_list,
)

urlpatterns = [
    path("products/", product_list, name="product_list"),
    path("product/<uuid:pk>/", product_detail, name="product_detail"),
    # path("wishlist/toggle/<uuid:pk>/", toggle_wishlist, name="toggle_wishlist"),
    # path("product/<uuid:pk>/ratings/", get_product_ratings_json, name="get_product_ratings_json"),
    # path("product/<uuid:pk>/comments/", get_product_comments_json, name="get_product_comments_json"),
]
