from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Genre, Movie


class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Название категории"
    }))
    slug = forms.SlugField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Slug"
    }))
    class Meta:
        model = Category
        fields = ['name','slug']


# class StudentForm(forms.Form):
#     name = forms.CharField(label="Имя студента", widget=forms.TextInput(attrs={"class": "student_input student_input2", }))
#     last_name = forms.CharField(label="Last name", required=False)
#     age = forms.IntegerField(label="Возраст студента", required=False)
#     email = forms.EmailField(label="Электронная почта", required=False, widget=forms.EmailInput(attrs={"class": "student_input student_input2", }))
#     phone_number = forms.CharField(label="Номер телефона")
#     group = forms.ModelChoiceField(label="Группа", queryset=Group.objects.all())
#     avatar = forms.ImageField(label="Аватарка", required=False)
#     tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
#     # join_date = forms.DateField(label="Дата присоединения")
#     # updated_date = forms.DateTimeField(label="Дата обновления")
#     is_active = forms.BooleanField(label="Активен", required=False)


class MovieForm(forms.ModelForm):
    name = forms.CharField(
        label="Название фильма", 
        widget=forms.TextInput(attrs={"class": "movie_input", })
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={"class": "movie_input", })
    )
    
    class Meta:
        model = Movie
        fields = '__all__'


class GenreForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Название Жанра"
    }))
    class Meta:
        model = Genre
        fields = ['name']
