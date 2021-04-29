from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name = "add_listing"),
    path("save_listing", views.save_listing, name = "save_listing"),
    path("item/<str:title>", views.listing_details, name = "listing_details"),
    path("post_bid", views.post_bid, name = 'post_bid'),
    path('save_comment', views.save_comment, name = 'save_comment'),
    path('category/<str:category>', views.categorized_listings, name = 'categorized_listings'),
    path('<str:user>/watchlist',views.watchlist, name= 'watchlist'),
]
