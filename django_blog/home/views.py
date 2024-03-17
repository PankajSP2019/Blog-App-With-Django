from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

# Models
from .models import Contact_H
from blog.models import Post

# For Sending Email, and Verified Email
from django.conf import settings
from .token import generate_token
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str


# Create your views here.


def home(request):
    # To show latest blog in home page
    last_three_blogs = Post.objects.all().order_by('-pno')[:3]
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


def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        user_name = request.POST['user_name']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        print(fname, lname, user_name, email, pass1, pass2)

        # Validation the form
        if len(user_name) < 8:
            messages.error(request, "The Length of User Name Should Not Be Less Than 8.")
            return redirect('Home')
        if not user_name.isalnum():
            messages.error(request, "User Name Should be Combination of Alphabet and Numerical Value, No Space. ")
            return redirect('Home')
        if pass1 != pass2:
            messages.error(request, "Password & Confirm Password Did Not Matched. ")
            return redirect('Home')

        #  If the User Exists OR not
        if User.objects.filter(username=user_name):
            messages.error(request, "Your Provided User Name is Already Exists, Please Try With Different User Name.")
            return redirect('Home')
        if User.objects.filter(email=email):
            messages.error(request, "Already Registered With This Email Address, Please Try With Different Email.")
            return redirect('Home')

        # user create
        user = User.objects.create_user(username=user_name, email=email, password=pass1)
        user.first_name = fname
        user.last_name = lname
        # Initially this user account will Deactivate
        # After email verification it will be Active
        user.is_active = False
        user.save()

        # Send Welcome Email

        # email verification

        messages.success(request, "Your Account Successfully Created.Please Check your email,and verified you account.")
        return redirect('Home')

    else:
        return HttpResponse("404 - You are not allowed.")


def logged_in(request):
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['userPassword']

        # Authenticate

        # Login

        print(username, password)

        return redirect('Home')
    else:
        return HttpResponse('404 - You Are Not Allowed')
