from django.urls import path
from .views import (
    blog_list, blog_detail, create_blog, edit_blog, delete_blog, toggle_like, add_comment, delete_comment
)

urlpatterns = [
    path('blogs/', blog_list, name='blog_list'),
    path('blog/<int:post_id>/', blog_detail, name='blog_detail'),
    path('create-blog/', create_blog, name='create_blog'),
    path('edit-blog/<int:post_id>/', edit_blog, name='edit_blog'),
    path('delete-blog/<int:post_id>/', delete_blog, name='delete_blog'),
    path('add-comment/<int:post_id>/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('toggle-like/<int:post_id>/', toggle_like, name='toggle_like'),
]
