from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path("commentpost/", views.postComment, name="CommentPost"),
    path("", views.blogHome, name="blogHome"),
    path("<str:slug>/", views.blogPost, name="blogPost"),


]
