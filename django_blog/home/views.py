from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Models
from .models import Contact_H
from blog.models import Post


# Create your views here.


def home(request):

    # To show latest blog in home page
    last_three_blogs = Post.objects.all().order_by('-pno')[:3]
    print(last_three_blogs)
    return render(request, 'home/home.html', {'latest_blog': last_three_blogs})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        content = request.POST.get('content')

        # Check Valid Email Address
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        email_check = re.match(pattern, email)

        # Validate the Form

        if (len(name) < 3) or (not email_check) or (len(phone) < 11) or (len(content) < 6):
            messages.error(request, "Please Provide Correct And Valid Information.")
            return redirect('Contact')
        else:
            c = Contact_H(name=name, email=email, phone=phone, content=content)
            c.save()
            messages.success(request, "You Successfully Drop Your Message, We will Contact Soon.")
            # messages.error(request, "Test")
            return redirect('Contact')

    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 100:
        # Create an Empty Queryset Object
        allpost = Post.objects.none()
    else:
        # Search in Title, Author, Content and Category
        allpost_title = Post.objects.filter(title__icontains=query)
        allpost_author = Post.objects.filter(author__icontains=query)
        allpost_content = Post.objects.filter(content__icontains=query)
        allpost_category = Post.objects.filter(category__icontains=query)

        # Marge All Searching result
        allpost = allpost_title.union(allpost_author, allpost_content, allpost_category)

    if allpost.count() == 0:
        messages.warning(request, "No Result Found")

    params = {'allpost': allpost, 'query': query}
    return render(request, "home/search.html", params)
