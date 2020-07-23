from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.CreatePage, name="CreatePage"),
    path("random",views.RandomPage, name="RandomPage"),
    path("search",views.SearchPage,name="SearchPage"),
    path("edit",views.EditPage, name="EditPage"),
    path("edit/<str:title>",views.EditPage, name="EditPage"),
    path("wiki/<str:title>", views.EntryPage, name="EntryPage"),


]
