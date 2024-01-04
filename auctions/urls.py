from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:id>", views.listing, name="listing"),
    path("<int:id>/bid", views.bid, name="bid"),
    path("<int:item_id>/watchlist_add", views.watchlist_add, name="add"),
    path("<int:watchlist_id>/watchlist_remove", views.watchlist_remove, name="remove"),
    path("<int:id>/close", views.close, name="close"),
    path("<int:id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.categoryList, name="category_list"),
    path("search", views.search, name="search"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("profile", views.profile, name="profile"),
]
