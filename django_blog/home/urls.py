from django.contrib import admin
# Custom Password Change View
from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from . import views
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm

urlpatterns = [
    path("", views.home, name="Home"),
    path("contact/", views.contact, name="Contact"),
    path("about/", views.about, name="About"),
    path("search/", views.search, name="Search"),
    path("register/", views.register, name="Register"),
    path("login/", views.logged_in, name="Login"),
    path("logout/", views.logout_blog, name="Logout"),
    path("activate/<uidb64>/<token>", views.activate_user, name="Activate"),
    path('checktiny', views.check_tiny, name="tiny"),
    path('authorRequest/', views.authorRequest, name="AuthorRequest"),
    path('author_request_handle/', views.author_request_handle, name="AuthorRequestHandle"),
    path('author_request_reject/', views.author_request_reject_handle, name="AuthorRequestRejectHandle"),
    path('author_request_accept/', views.author_request_accept_handle, name="AuthorRequestAcceptHandle"),
    path('author_panel/', views.author_panel, name="AuthorPanel"),
    path('password_change/', views.password_change, name="PasswordChange"),
    path('reset_password_request/', views.reset_password_request, name="ResetPasswordRequest"),
    path('reset/<uidb64>/<token>', views.reset_password_confirm, name='ResetPasswordConfirm'),

    # Another Approach To Change Password
    # path('password_change/', PasswordChangeView.as_view(
    #     template_name='home/password_change.html',
    #     success_url=reverse_lazy('Home'),
    #     form_class=CustomPasswordChangeForm
    # ),
    #      name="PasswordChange"),

]
