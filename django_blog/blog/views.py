from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.


def blogHome(request):
    allPost = Post.objects.all()
    context = {'allpost': allPost}
    return render(request, "blog/bloghome.html", context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    context = {'post': post}
    return render(request, "blog/blogpost.html", context)

