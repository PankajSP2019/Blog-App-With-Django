from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, BlogComment
from django.contrib import messages


# Create your views here.


def blogHome(request):
    allPost = Post.objects.all()
    context = {'allpost': allPost}
    return render(request, "blog/bloghome.html", context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    if post is not None:
        comments = BlogComment.objects.filter(post=post).order_by('-timestamp')
        context = {'post': post, 'comments': comments}
        return render(request, "blog/blogpost.html", context)
    else:
        return HttpResponse("404 - Some Error Occurs")


def postComment(request):
    print('hello')
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        post_pno = request.POST.get('post_pno')
        post = Post.objects.get(pno=post_pno)

        comment_insert = BlogComment(comment=comment, user=user, post=post)
        comment_insert.save()

        messages.success(request, "Your Comment Has Been Posted..")
        # return redirect(f"/blog/{post.slug}")
        return redirect("blogPost", slug=post.slug)

    else:
        return HttpResponse("404 - Some Error Occurs")
