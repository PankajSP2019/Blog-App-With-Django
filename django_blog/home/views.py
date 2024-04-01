from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# For Give Permission To User
from django.contrib.auth.models import Permission

# Models
from .models import Contact_H, UserProfile, AuthorRequest
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

    if len(query) == 0:
        return redirect('blogHome')

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
        # Few Changes to For upload Files, without Django File System
        profile_picture = request.FILES.get("profile_picture")

        # print(fname, lname, user_name, email, pass1, pass2)

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
        user = User.objects.create_user(username=user_name.lower(), email=email, password=pass1)
        user.first_name = fname
        user.last_name = lname
        # Initially this user account will Deactivate
        # After email verification it will be Active
        user.is_active = False
        user.save()

        # User Profile
        user_profile = UserProfile(user=user, profile_picture=profile_picture)
        user_profile.save()

        # Send Welcome Email & Email Verification
        current_site = get_current_site(request)
        subject = "Welcome to BlogSphere - Activate Your Account Now!."
        message = render_to_string('home/email_confirmation.html', {
            'name': f"{user.first_name} {user.last_name}",
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.fail_silently = True
        email.send()

        messages.success(request, "Your Account Successfully Created.Please Check your email,and verified(Active) you "
                                  "account.")
        # return redirect('Home')
        # It Redirect to the Same page From Where This Request Call
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponse("404 - You are not allowed.")


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(user, token):
        if user.is_active:
            messages.warning(request, "Your Account is Already Activated.")
            return redirect('Home')
        else:
            user.is_active = True
            user.save()
            messages.success(request, "Your Account is Activated. Now, You Can Login To Your Account With User Name & "
                                      "Password.. ")
            return redirect('Home')
    else:
        return HttpResponse(f"Something Went Wrong, Please Inform Our Admin.")


def logged_in(request):
    if request.method == 'POST':

        if request.user.is_authenticated:
            messages.error(request, "You Are Already Logged in With an Account..")
            # return redirect('Home')
            # It Redirect to the Same page From Where This Request Call
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        username = request.POST['userName']
        password = request.POST['userPassword']

        # Authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            # Login
            login(request, user)
            messages.success(request, "Successfully Logged In...")
            #  return redirect('Home')
            # It Redirect to the Same page From Where This Request Call
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Wrong Credential, Please Try Again..")
            # return redirect('Home')
            # It Redirect to the Same page From Where This Request Call
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # print(username, password)
    else:
        return HttpResponse('404 - You Are Not Allowed')


@login_required(login_url="/")
def logout_blog(request):
    logout(request)
    messages.success(request, "Successfully Logged Out, Thank You.")
    #  return redirect('Home')
    # It Redirect to the Same page From Where This Request Call
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/")
def authorRequest(request):
    if request.method == 'POST':
        about_author = request.POST['about_author']
        if len(about_author) > 20:
            author_request = AuthorRequest(user=request.user, about_author=about_author, status='Pending')
            author_request.save()

            messages.success(request, "Your Request Is Submitted To Our Admin. Wait For Confirmation.")
            # It Redirects to the Same page From Where This Request Call
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.warning(request, "Your Description Is Too Short.")
            # It Redirects to the Same page From Where This Request Call
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("Something Went Wrong")


def author_request_handle(request):
    all_author_request = AuthorRequest.objects.all()
    return render(request, "home/author_request_handle.html", {'all_author_request': all_author_request})


def author_request_reject_handle(request):
    # We can use here request.user.is_authenticated
    if request.method == "POST":
        reject_reason = request.POST['reject_reason']
        print(reject_reason)

        # Author Reject Operation

        messages.warning(request, "Successfully Reject Author Request.")
        return redirect('AuthorRequestHandle')
    else:
        return HttpResponse("Something Went Wrong Please Contact Our Admin.")


def author_request_accept_handle(request):
    # We can use here request.user.is_authenticated
    if request.method == "POST":
        add_p = request.POST.get('add_perms', 'off')
        view_p = request.POST.get('view_perms', 'off')
        delete_p = request.POST.get('delete_perms', 'off')
        change_p = request.POST.get('change_perms', 'off')
        if add_p == 'off' and view_p == 'off' and delete_p == 'off' and change_p == 'off':
            messages.error(request, "You Have To Grant At least 1 Permission.")
            return redirect('AuthorRequestHandle')
        else:
            # Give Permission Will here
            if add_p == 'on':
                print("Add Permission Give Here")
            if view_p == 'on':
                print("View Permission Give Here")
            if delete_p == 'on':
                print("Delete Permission Give Here")
            if change_p == 'on':
                print("Change Permission Give Here")

        # Author Accept Operation

        messages.success(request, "Successfully Accept Author Request.")
        return redirect('AuthorRequestHandle')
    else:
        return HttpResponse("Something Went Wrong Please Contact Our Admin.")


def check_tiny(request):
    return render(request, "tinyMCE_example.html")
