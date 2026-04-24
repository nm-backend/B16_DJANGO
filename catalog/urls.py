from django.urls import path

from . import views
from .views import add_category, add_genre, category_detail, delete_movie

urlpatterns = [
    path('main/', views.MainPageView.as_view(), name='main_page'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('category/<str:slug>/', category_detail, name='category_detail'),
    path("add-movie/", views.MovieCreateView.as_view(), name="add_movie"),
    path("add-category/", add_category, name="add_category"),
    path("add-genre/", add_genre, name="add_genre"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("change-movie/<int:pk>/", views.MovieUpdateView.as_view(), name="change_movie"),
    path("delete-movie/<int:pk>/", delete_movie, name="delete_movie")
]