from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path(
        "listing_page/<int:listing_id>/<path:name_to_save>/<str:message>",
        views.listing_page,
        name="listing_page",
    ),
    path("watchlist/<str:action>", views.watchlist, name="watchlist"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("my_listings/<str:action>", views.my_listings, name="my_listings"),
    path("categories/<str:action>/<str:category>", views.categories, name="categories"),
    path("<path:anything>", views.not_found, name="not_found"),
]

urlpatterns += staticfiles_urlpatterns()
