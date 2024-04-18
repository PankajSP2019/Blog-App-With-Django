from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, BlogComment
from django.contrib import messages

# Check Permission
from django.contrib.auth.decorators import permission_required, login_required


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


# Post A Blog By Author
@permission_required("blog.add_post", login_url="/")  # Check The add permission
def PostBlog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        image = request.FILES.get("main-image")
        blog_content = request.POST['blog-content']
        blog_summary = request.POST['blog-summary']
        fname = request.user.first_name
        lname = request.user.last_name
        author_name = f"{fname} {lname}"
        user = request.user

        # Validation

        # For Title
        if len(title) < 20:
            messages.error(request, "Blog Title Is Too Short Less Than 20 Character.")
            return redirect('PostBlog')

        # For Image
        # We Just Allowed to Upload Image file, Using Html
        # If Anyone, Tries To Upload Non Image file, For This Validate In Here, Detect The File Image Or Not
        import imghdr
        image_type = imghdr.what(image)
        if not image_type:
            messages.error(request, "You Are Allowed To Upload Image File, As Main Image.")
            return redirect('PostBlog')

        # For Blog Content
        if len(blog_content) < 1500:
            messages.error(request, "Blog Content Is Too Short Less Than 1000 Character.")
            return redirect('PostBlog')

        # For Blog Summary
        if len(blog_summary) < 300:
            messages.error(request, "Blog Content Is Too Short Less Than 300 Character.")
            return redirect('PostBlog')

        # Insert The Blog
        post_blog = Post(title=title, author=author_name, user=user, category=category,
                         content=blog_content, summary=blog_summary, image=image)
        post_blog.save()

        # print(title, category, image, blog_content, blog_summary)
        # print(author_name, user)

        messages.success(request, "Post Blog Successfully.")
        return redirect('PostBlog')

    return render(request, "home/add_blog.html")
