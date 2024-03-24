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
        comments = BlogComment.objects.filter(post=post, parent=None).order_by('-timestamp')
        # exclude(parent=None) , This will not fetch value, which parent is None
        replies = BlogComment.objects.filter(post=post).exclude(parent=None)
        reply_dict = {}
        for reply in replies:
            if reply.parent.cno not in reply_dict.keys():
                reply_dict[reply.parent.cno] = [reply]
            else:
                reply_dict[reply.parent.cno].append(reply)
        context = {'post': post, 'comments': comments, 'reply_dict': reply_dict}
        return render(request, "blog/blogpost.html", context)
    else:
        return HttpResponse("404 - Some Error Occurs")


def postComment(request):
    print('hello')
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        post_pno = request.POST.get('post_pno')
        parent_comment_cno = request.POST.get('parentPno')
        post = Post.objects.get(pno=post_pno)

        # Check It is a comment or reply
        if parent_comment_cno == "":
            # It's a Comment
            comment_insert = BlogComment(comment=comment, user=user, post=post)
            comment_insert.save()
            messages.success(request, "Your Comment Has Been Posted..")
            # return redirect(f"/blog/{post.slug}")
            return redirect("blogPost", slug=post.slug)
        else:
            # It's a Reply
            parent = BlogComment.objects.get(cno=parent_comment_cno)
            comment_insert = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment_insert.save()
            messages.success(request, "Your Reply Has Been Posted..")
            # return redirect(f"/blog/{post.slug}")
            return redirect("blogPost", slug=post.slug)

    else:
        return HttpResponse("404 - Some Error Occurs")
