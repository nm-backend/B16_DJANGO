from rest_framework.decorators import api_view
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from catalog.models import Category, Genre, Movie

from .serializers import (
    CategoryModelSerializer,
    GenreModelSerializer,
    MovieModelSerializer,
    MovieSerializer,
)


class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# @api_view(["GET", "POST"])
# def movies_list(request):
#     if request.method == "GET":
#         movies_list = Movie.objects.all()
#         serializer = MovieModelSerializer(movies_list, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = MovieModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         print(serializer.errors)
#         return Response(serializer.errors, status=400)

class MoviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer
    

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({"datail": "Not Fount"})

    if request.method == "GET":
        serializer = MovieModelSerializer(movie, many=False)
        return Response(serializer.data)
    
    if request.method == "PUT":
        serializer = MovieModelSerializer(movie, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    if request.method == "DELETE":
        movie.delete()
        return Response(status=204)
    


@api_view(["GET", "POST"])
def categories_list(request):
    if request.method == "GET":
        categories_list = Category.objects.all()
        serializer = CategoryModelSerializer(categories_list, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)
    

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"datail": "Not Fount"})

    if request.method == "GET":
        serializer = CategoryModelSerializer(category, many=False)
        return Response(serializer.data)
    
    if request.method == "PUT":
        serializer = CategoryModelSerializer(category, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    if request.method == "DELETE":
        category.delete()
        return Response(status=204)
    

@api_view(["GET", "POST"])
def genres_list(request):
    if request.method == "GET":
        genres_list = Genre.objects.all()
        serializer = GenreModelSerializer(genres_list, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = GenreModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)
    

@api_view(['GET', 'PUT', 'DELETE'])
def genre_detail(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
    except Genre.DoesNotExist:
        return Response({"datail": "Not Fount"})

    if request.method == "GET":
        serializer = GenreModelSerializer(genre, many=False)
        return Response(serializer.data)
    
    if request.method == "PUT":
        serializer = GenreModelSerializer(genre, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    if request.method == "DELETE":
        genre.delete()
        return Response(status=204)
    
