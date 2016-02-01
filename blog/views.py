from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .forms import FormForPost


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # posts now is like QuerySet
    return render(request, 'blog/post_list.html', {'posts': posts})


# Show only single post.Else - 404
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


# For creating new post
def post_new(request):
    if request.method == "POST":
        form = FormForPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', post_id=post.pk)
    else:
        form = FormForPost()
    return render(request, 'blog/post_edit.html', {'form': form})


# For correcting post
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = FormForPost(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', post_id=post.pk)
    else:
        form = FormForPost(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

