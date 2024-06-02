from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

# For Give Permission To User
from django.contrib.auth.models import Permission

# For Use Multiple Condition In QuerySet - > Filter
from django.db.models import Q

# Models
from .models import Contact_H, UserProfile, AuthorRequest
from blog.models import Post

# For Sending Email, and Verified Email
from django.conf import settings
from .token import generate_token, account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

# For Password Change Default Form
# from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

# After Change the Password The Session Is Reset Automatically, Update the Session
from django.contrib.auth import update_session_auth_hash

# Custom Form For Password Change
from .forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

from typing import Protocol


# Create your views here


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

            # Set custom Sessions To Check The User Author OR Not
            user_profiles = UserProfile.objects.filter(user=user.pk)
            if user_profiles.exists():
                user_profile = user_profiles[0]
                request.session['is_author'] = user_profile.is_author

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

    # Remove the Custom Session
    request.session.clear()
    request.session.flush()

    messages.success(request, "Successfully Logged Out, Thank You.")
    #  return redirect('Home')
    # It Redirect to the Same page From Where This Request Call
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/")
def authorRequest(request):
    if request.method == 'POST':
        # if not AuthorRequest.objects.filter(user=request.user).exists():
        # Using Multiple condition in filter object
        if not AuthorRequest.objects.filter(
                Q(user=request.user) & (Q(status='Pending') | Q(status='Accepted'))).exists():
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
            check = AuthorRequest.objects.filter(user=request.user).first()
            if check.status == "Pending":
                messages.error(request, "You Are Already Requested For Author And Status Is :  Pending")
                # It Redirects to the Same page From Where This Request Call
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,
                               "You Are Already An Author, Why You are Request Again, If You Face Any Problem Please Contact With Our Admin.. ")
                # It Redirects to the Same page From Where This Request Call
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("Something Went Wrong")


# Show All Author Request Information To Super User/Admin Only
@login_required(login_url="/")
def author_request_handle(request):
    if request.user.is_superuser:

        # Pending Author Request
        all_author_request = AuthorRequest.objects.filter(status="Pending")

        # Just For Show The Author List And Their Blog Count
        # Author List
        author_list = UserProfile.objects.filter(is_author=True)
        print(author_list)

        # Author's Blog Count
        author_blog_count = []
        for i in author_list:
            blog_count = Post.objects.filter(user=i.user).count()
            author_blog_count.append([f"{i.user.first_name} {i.user.last_name}",blog_count])

        return render(request, "home/author_request_handle.html", {'author_requests': all_author_request, 'author_blog_count': author_blog_count})
    else:
        messages.error(request, "You Are Not Allowed To Visit This Page.")
        # It Redirects to the Same page From Where This Request Call
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# This Function Is For Author Request Rejection
@login_required(login_url="/")
def author_request_reject_handle(request):
    """
    :param request:
    :return: Status of the author request will be rejected, and send a rejection mail to author's email address.
    """
    # We can use here request.user.is_authenticated
    if request.method == "POST":
        reject_reason = request.POST['reject_reason']
        ar_no = request.POST['ar_no']
        ar_user_pk = request.POST['ar_user']

        # Author Reject Operation
        au_re = AuthorRequest.objects.filter(ar_no=ar_no, user=ar_user_pk).exclude(status="Rejected")[0]
        # au_re = AuthorRequest.objects.filter(ar_no=ar_no, user=ar_user_pk, status="Pending")
        au_re.reject_reason = reject_reason
        au_re.status = "Rejected"
        au_re.save()

        # Send Email To Author, Inform That His/Her Author Request Is Rejected.
        user = User.objects.filter(pk=ar_user_pk)[0]

        # Email message, Yes Its messy, Please Ignore it.
        reject_message = f"""Thank you for your interest in becoming an author for BlogSphere. We appreciate the time and effort you invested in your application and your enthusiasm for contributing to our platform.
        
After careful consideration, we regret to inform you that we have decided not to move forward with your application at this time. This decision was not made lightly, and it reflects our current needs and priorities for the blog.
        
Reject Reason : {reject_reason}

Please understand that this is not a reflection of your abilities or potential. We encourage you to continue pursuing your passion for writing and to keep us in mind for future opportunities.
        
If you have any questions or would like feedback on your application, please feel free to reach out. We wish you the best in your future endeavors and hope to see you as a valued member of our reader community."""

        subject = "Regarding Author Request-BlogSphere."
        message = render_to_string('home/author_request_handle_mail.html', {
            'name': f"{user.first_name} {user.last_name}",
            'message': reject_message,
            'ar_no': ar_no,

        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.fail_silently = True
        email.send()

        messages.warning(request, f"Request No. {ar_no}. Successfully Reject Author Request.")
        return redirect('AuthorRequestHandle')
    else:
        return HttpResponse("Something Went Wrong Please Contact Our Admin.")


@login_required(login_url="/")
def author_request_accept_handle(request):
    # We can use here request.user.is_authenticated
    if request.method == "POST":
        add_p = request.POST.get('add_perms', 'off')
        view_p = request.POST.get('view_perms', 'off')
        delete_p = request.POST.get('delete_perms', 'off')
        change_p = request.POST.get('change_perms', 'off')
        ar_no = request.POST['ar_no']
        ar_user = request.POST['ar_user']
        ar_user_pk = request.POST['ar_user_pk']

        if add_p == 'off' and view_p == 'off' and delete_p == 'off' and change_p == 'off':
            messages.error(request, "You Have To Grant At least 1 Permission.")
            return redirect('AuthorRequestHandle')
        else:
            # Give Permission Will here
            user = User.objects.get(pk=ar_user_pk)
            permission_list = []
            if add_p == 'on':
                permission_list.append("Add Permission")
                add_blog_permission = Permission.objects.get(name="Can add post")
                user.user_permissions.add(add_blog_permission)
            if view_p == 'on':
                permission_list.append("View Permission")
                view_blog_permission = Permission.objects.get(name="Can view post")
                user.user_permissions.add(view_blog_permission)
            if delete_p == 'on':
                permission_list.append("Delete Permission")
                delete_blog_permission = Permission.objects.get(name="Can delete post")
                user.user_permissions.add(delete_blog_permission)
            if change_p == 'on':
                permission_list.append("Change Permission")
                change_blog_permission = Permission.objects.get(name="Can change post")
                user.user_permissions.add(change_blog_permission)

            user.save()

            # User Profile Update to Is_Author
            make_author = UserProfile.objects.get(user=ar_user_pk)
            make_author.is_author = True
            make_author.save()

            # Author Accept Operation
            au_re = AuthorRequest.objects.filter(ar_no=ar_no, user=ar_user_pk, status="Pending")[0]
            au_re.status = "Accepted"
            au_re.save()

            # Send Email To Author, Inform That His/Her Author Request Is Accepted.
            user = User.objects.filter(pk=ar_user_pk)[0]

            # Email message, Yes Its messy, Please Ignore it.
            accept_message = f"""We are pleased to inform you that your Request to become an author for BlogSphere has been accepted!

Now, you have the access of Author Panel, where you can show your creativity.

Permission List : {permission_list}

Welcome aboard! We look forward to your contributions. If you have any questions, feel free to reach out.
"""

            subject = "Regarding Author Request-BlogSphere."
            message = render_to_string('home/author_request_handle_mail.html', {
                'name': f"{user.first_name} {user.last_name}",
                'message': accept_message,
                'ar_no': ar_no

            })
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.fail_silently = True
            email.send()

        messages.success(request, "Successfully Accept Author Request.")
        return redirect('AuthorRequestHandle')
    else:
        return HttpResponse("Something Went Wrong Please Contact Our Admin.")


# Author Panel
@login_required(login_url="/")
def author_panel(request):
    if (request.user.has_perm('blog.add_post') or request.user.has_perm('blog.change_post') or
            request.user.has_perm('blog.delete_post') or request.user.has_perm('blog.view_post')):
        authors_all_blog = Post.objects.filter(user=request.user)
        if len(authors_all_blog) == 0:
            messages.warning(request, "You Have No Post Exits. Please Post Your Blog.")
            return render(request, "home/author_panel.html")
        else:
            print(len(authors_all_blog))
            return render(request, "home/author_panel.html", {'authors_all_blog': authors_all_blog})

    else:
        messages.error(request, "You Have No Permission, You Are Not Allowed In Author Panel.")
        return redirect('Home')


@login_required(login_url="/")
# For Change The User Password
def password_change(request):
    """
    :param request:
    :return: Show The Password Change Form and If User Request, Change The Password
    """

    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request, "Your Password Change Successfully..")
            return redirect("Home")
    else:
        # Password Change Form
        fm = PasswordChangeForm(user=request.user)

    return render(request, "home/password_change.html", {'fm': fm})


#  For Reset The Password
def reset_password_request(request):
    """
    :param request:
    :return: Send Email To User's Mail Account, With Some Instruction For Reset The Password
    """

    if request.user.is_authenticated:
        messages.error(request, "You are not allowed to reset password, while you are logged in.")
        return redirect('Home')

    if request.method == 'POST':
        fm = PasswordResetForm(request.POST)
        if fm.is_valid():
            # Fetch Data From From
            user_email = fm.cleaned_data['email']
            user = User.objects.filter(email=user_email).first()
            # user = get_user_model().objects.filter(email=user_email).first()

            if user:

                if not user.is_active:
                    messages.error(request, "Your are not active user, Please active your account first.")
                    return redirect('Home')

                # Send Instruction Email To User For Reset Password
                current_site = get_current_site(request)
                subject = "Password Reset Request."
                message = render_to_string('home/password_reset_email_template.html', {
                    'name': f"{user.first_name} {user.last_name}",
                    'username': f"{user.username}",
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                email.fail_silently = True
                # email.send()

                if email.send():
                    messages.success(request, """
                        <h4>Password Reset Instruction</h4><hr>
                        <p> 
                            We've sent you an email with instructions on how to set your password, provided there's an 
                            account associated with the email you entered. You should receive it soon.<br>If you don't 
                            see the email, please double-check that you've entered the email address you used to 
                            register, and take a look in your spam folder.
                        </p>
                    """)
                else:
                    messages.error(request, "Problem Sending Reset Password Email, <b>SERVER PROBLEM</b>")
                return redirect('Home')
            else:
                messages.error(request, f"""
                <h4>Email Not Found</h4><hr>
                <p>{user_email} - This Email Is Not Associate With Any User. Please Try Again.</p>
                """)
                return redirect('Home')
        else:
            messages.error(request, "Something Went Wrong For Reset The Password. Please Try Again.")
            return redirect('Home')
    else:
        fm = PasswordResetForm()

    return render(request, "home/reset_password_request.html", {'fm': fm})


def reset_password_confirm(request, uidb64, token):
    if request.user.is_authenticated:
        messages.error(request, "You are not allowed to reset password, while you are logged in.")
        return redirect('Home')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(user, token):

        if request.method == 'POST':
            fm = SetPasswordForm(user, request.POST)
            if fm.is_valid():
                fm.save()

                messages.success(request, "Your New Password Has Been Set Success Fully. Now You Can Login With Your "
                                          "New Password.")
                return redirect('Home')
            else:
                for error in list(fm.errors.values()):
                    messages.error(request, error)

        fm = SetPasswordForm(user)
        return render(request, 'home/password_reset_confirm.html', {'fm': fm})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, "Something Went Wrong Reset Your Passwords, Please Try Aging.")
    return redirect('Home')


def check_tiny(request):
    return render(request, "tinyMCE_example.html")


def testing(request):
    last_three_blogs = Post.objects.all().order_by('-pno')[:3]
    return render(request, 'testing.html', {'latest_blog': last_three_blogs})
