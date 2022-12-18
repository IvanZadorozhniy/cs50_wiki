from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search/", views.search_request, name="search"),
    path("create_article", views.create_article, name="create_article"),
    path("random_article", views.random_article, name="random_article"),
    path("edit_article/<str:title>", views.edit_article, name="edit_article"),
    

]
