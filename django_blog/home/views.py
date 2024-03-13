from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Models
from .models import Contact_H


# Create your views here.


def home(request):
    return render(request, 'home/home.html')


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
