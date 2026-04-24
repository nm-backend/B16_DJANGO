from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from catalog.models import Category, Genre, Movie


class MovieModelSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    
class GenreModelSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=250)
    description = serializers.CharField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=False)
    directed_by = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    age_rating = serializers.CharField(max_length=10)
    raiting = serializers.IntegerField()
    image = serializers.ImageField(required=False)
    trailir_video = serializers.FileField(required=False)
    budget = serializers.IntegerField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        # instance.genres.set(validated_data.get('genre', instance.genres.all()))
        instance.directed_by = validated_data.get('directed_by', instance.directed_by)
        instance.country = validated_data.get('country', instance.country)
        instance.age_rating = validated_data.get('age_rating', instance.age_rating)
        instance.raiting = validated_data.get('raiting', instance.raiting)
        instance.image = validated_data.get('image', instance.image)
        instance.budget = validated_data.get('budget', instance.budget)
        instance.trailir_video = validated_data.get('trailir_video', instance.trailir_video)
        instance.save()
        return instance