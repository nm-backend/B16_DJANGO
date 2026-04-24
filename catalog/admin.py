from django.contrib import admin

# Register your models here.
from .models import Category, Genre, Movie


class MovieInline(admin.TabularInline):
    model = Movie
    extra = 0



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [MovieInline]
    list_display = ['id','name','slug','count_movies']
    search_fields = ['name',]
    ordering = ['id']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['id',  'name','created_date','country','raiting',]
    # ordering = ['id']
    list_filter = ['category', 'genres']
    # readonly_fields = ['get_image']

    
    # @admin.display(description="Изображение")
    # def get_image(self,movie):
    #     text = mark_safe(f'<img scr={movie.image.url if movie.image else "-"} width="150px" />')
    #     return text
    
    

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

