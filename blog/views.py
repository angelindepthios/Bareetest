from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm
from django.db.models import Q

def blog_list(request):
    query = request.GET.get("q")  # Get the search query from the request
    blogs = BlogPost.objects.all().order_by('-created_at')

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) | 
            Q(author__username__icontains=query) | 
            Q(content__icontains=query)
        )

    return render(request, 'blog_list.html', {'blogs': blogs, 'query': query})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all()
    return render(request, 'blog_detail.html', {'post': post, 'comments': comments})

@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)  
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog_form.html', {'form': form})

@login_required
def edit_blog(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=blog)  # Handle file updates
        if form.is_valid():
            form.save()
            return redirect('blog_detail', post_id=blog.id)
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def delete_blog(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == "POST":
        blog.delete()
        return redirect('blog_list')
    return render(request, 'confirm_delete.html', {'blog': blog})

@login_required(login_url='/login/')
def toggle_like(request, post_id):
    if request.method == "POST":
        user = request.user
        post = get_object_or_404(BlogPost, pk=post_id)

        if post.likes.filter(id=user.id).exists():  # If already liked, unlike it
            post.likes.remove(user)
            liked = False
        else:  # If not liked, like it
            post.likes.add(user)
            liked = True

        return JsonResponse({"liked": liked, "total_likes": post.likes.count()})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required(login_url='/login/')
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return JsonResponse({
                "message": "Comment submitted successfully!",
                "author": comment.author.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%b %d, %Y - %I:%M %p"),
                "comment_id": comment.id
            })

        return JsonResponse({"errors": form.errors}, status=400)

    return redirect('blog_detail', post_id=post.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author:
        comment.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "You are not authorized to delete this comment"}, status=403)

