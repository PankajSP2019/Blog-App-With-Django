from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("contact/", views.contact, name="Contact"),
    path("about/", views.about, name="About"),
    path("search/", views.search, name="Search"),
    path("register/", views.register, name="Register"),
    path("login/", views.logged_in, name="Login"),
    path("logout/", views.logout_blog, name="Logout"),
    path("activate/<uidb64>/<token>", views.activate_user, name="Activate"),
    path('checktiny', views.check_tiny, name="tiny")

]
