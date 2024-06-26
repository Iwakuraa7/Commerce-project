from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("categories", views.category_view, name="category"),
    path("watchlist", views.watchlist_view, name="watchlist"),
]
