from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import movies_list, movie_detail, categories_list, category_detail, genres_list, genre_detail
from . import views
from . import viewsets

router = DefaultRouter()
router.register('movies', viewsets.MovieViewSet)

urlpatterns = [
    path('', include('api.yasg')),
    path("auth/", include("api.auth.urls")),
    path('', include(router.urls)),
#     # path("movies/", movies_list),
#     path("movies/", views.MovieListCreateAPIView.as_view()),
#     # path("movies/<int:pk>/", views.movie_detail),
#     path("movies/<int:pk>/", views.MovieRetrieveUpdateDestroyAPIView.as_view()),
#     path("categories/", views.categories_list),
#     path("categories/<int:pk>/", views.category_detail),
#     path("genres/", views.genres_list),
#     path("genres/<int:pk>/", views.genre_detail),
]