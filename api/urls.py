from django.urls import include, path

# from .views import movies_list, movie_detail, categories_list, category_detail, genres_list, genre_detail
from . import views

urlpatterns = [
    path('', include('api.yasg')),
    path("auth/", include("api.auth.urls")),
    # path("movies/", movies_list),
    path("movies/", views.MovieListCreateAPIView.as_view()),
    # path("movies/<int:pk>/", views.movie_detail),
    path("movies/<int:pk>/", views.MoviewRetrieveUpdateDestroyAPIView.as_view()),
    path("categories/", views.categories_list),
    path("categories/<int:pk>/", views.category_detail),
    path("genres/", views.genres_list),
    path("genres/<int:pk>/", views.genre_detail),
]