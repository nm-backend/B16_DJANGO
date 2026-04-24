from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import CategoryForm, GenreForm, MovieForm
from .models import Category, Genre, Movie


class MainPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["movies"] = Movie.objects.all()
        context['categories'] = Category.objects.all()

        return context


# def main_page(request):
#     categories = Category.objects.all()
#     genres = Genre.objects.all()
    
#     query = request.GET.get('q')
#     movies = Movie.objects.all()  # по умолчанию пусто

#     if query:
#         movies = Movie.objects.filter(name__icontains=query)

    
#     page_number = request.GET.get('page', 1)  # текущая страница, по умолчанию 1
#     paginator = Paginator(movies, 3)  # показываем 9 фильмов на странице
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'categories': categories,
#         'movies': page_obj,  # передаем уже страницу с объектами
#         'genres': genres,
#         'query': query,
#     }
#     return render(request, 'index.html', context)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


# def movie_detail(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     return render(request, 'movie_detail.html', context={'movie': movie})


class MovieCreateView(CreateView):
    template_name = "add_movie.html"
    form_class = MovieForm
    model = Movie
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        # context['categories'] = Category.objects.all()
        return context


class MovieUpdateView(UpdateView): 
    model = Movie
    form_class = MovieForm
    template_name = "add_movie.html"
    context_object_name = "movie"

    def get_success_url(self):
        # Redirect back to the detail page of the updated movie
        return reverse_lazy('movie_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        # context['categories'] = Category.objects.all()
        context['is_edit'] = True 
        return context



# def add_movie(request):
#     categories = Category.objects.all()
#     genres = Genre.objects.all()

#     if request.method == "POST":
#         form = MovieForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("main_page")
#     else:
#         form = MovieForm()

#     return render(request, "add_movie.html", {
#         "categories": categories,
#         "genres": genres,
#         "form": form
#     })


def category_detail(request,slug):
    category = get_object_or_404(Category,slug=slug)
    movies = Movie.objects.filter(category=category)
    query = request.GET.get('q')

    if query:
        movies = Movie.objects.filter(name__icontains=query)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(movies, 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'category':category,
        'movies':page_obj,
        'query':query
    }
    return render(request,'category_detail.html',context=context)


def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()

    return redirect("main_page")


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main_page")
    else:
        form = CategoryForm()
        
    return render(request, "add_category.html", context={"form": form})


def add_genre(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main_page")
    else:
        form = GenreForm()

    return render(request, "add_genre.html", context={"form": form})
    

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "auth/register.html", {
                "error": "Пароли не совпадают"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "auth/register.html", {
                "error": "Такой пользователь уже есть"
            })

        User.objects.create_user(
            email=email,
            password=password
        )

        return redirect("main_page")

    return render(request, "auth/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("main_page")
        else:
            return render(request, "auth/login.html", {
                "error": "Неверный логин или пароль"
            })

    return render(request, "auth/login.html")


# class MovieUpdateView(UpdateView):
#     template_name = "add_movie.html"
#     model = Movie



# def change_movie(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     categories = Category.objects.all()
#     genres = Genre.objects.all()

#     if request.method == "POST":
#         movie.name = request.POST.get("name")
#         movie.description = request.POST.get("description")
#         movie.country = request.POST.get("country")
#         movie.directed_by = request.POST.get("directed_by")
#         movie.age_rating = request.POST.get("age_rating")
#         movie.raiting = request.POST.get("raiting") or movie.raiting
#         movie.category_id = request.POST.get("category")

#         image = request.FILES.get("image")
#         trailir_video = request.FILES.get("trailir_video")
#         if image:
#             movie.image = image
#         if trailir_video:
#             movie.trailir_video = trailir_video

#         movie.save()
#         movie.genre.set(request.POST.getlist("genres"))

#         return redirect("movie_detail", pk=movie.pk)

#     return render(request, "add_movie.html", {
#         "categories": categories,
#         "genres": genres,
#         "movie": movie,
#         # "movie_genre_ids": set(movie.genre.values_list("id", flat=True)),
#         "movie_genre_ids": {2, 3},
#         "is_edit": True,
#     })

