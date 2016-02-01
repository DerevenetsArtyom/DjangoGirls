from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .forms import FormForPost


def post_list(request):
    posts = Post.objects.order_by('published_date')
    # posts now is like QuerySet
    return render(request, 'blog/post_list.html', {'posts': posts})


# Show only single post.Else - 404
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


# For creating new post
def post_new(request):
    if request.method == "POST":
        # Client try to refill/change the form
        # 'load' some data from POST
        form = FormForPost(request.POST)
        # form validation
        if form.is_valid():
            # We don't want to save form yet
            # WE add author at the next step
            post = form.save(commit=False)  # commit responsible for it
            # save user as author
            post.author = request.user
            post.save()
            # Immediate redirect to created form detail
            return redirect('blog.views.post_detail', post_id=post.pk)
    else:
        # This is the case, when we fill in our form FIRST TIME
        # We wanted to get clear form
        form = FormForPost()
    return render(request, 'blog/post_edit.html', {'form': form})


# For correcting existed post
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

