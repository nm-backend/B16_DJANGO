from rest_framework.viewsets import ModelViewSet

from catalog.models import Movie, Category, Genre, MovieImage
from .serializers import (
    MovieModelSerializer,
    MovieCreateUpdateSerializer, MovieDetailSerializer
)

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return MovieCreateUpdateSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
        elif self.action == 'list':
            return MovieModelSerializer
        return MovieModelSerializer