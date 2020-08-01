from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inactive", views.inactive, name="inactive"),
    path("create", views.create, name="create"),
    path("WatchList",views.WatchList , name="WatchList"),
    path('addBid/<int:list>',views.addBid , name = 'addBid'),
    path('category/<str:category>',views.category , name = 'category'),
    path("listing/<int:number>", views.listing, name="listing"),
    path("listing/<int:number>/<str:message>", views.listing, name="listing"),
    path("closeBid/<int:number>", views.closeBid, name="closeBid"),
    path("comment/<int:number>", views.comment, name="comment"),
    path("WatchList/<int:item>",views.WatchList , name="WatchList"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
