import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Movie


@receiver(post_delete, sender=Movie)
def delete_movie_files(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    if instance.trailir_video:
        if os.path.isfile(instance.trailir_video.path):
            os.remove(instance.trailir_video.path)


@receiver(pre_save, sender=Movie)
def check_raiting(sender, instance, **kwargs):
    if instance.raiting > 5:
        instance.raiting = 5

# Задание 2 — Проверка рейтинга перед сохранением
# Задача
# Перед сохранением фильма проверить рейтинг.

# Если:
# rating > 5

# установить:
# rating = 5

# Если:
# rating < 0

# установить:
# rating = 0

# Использовать
# pre_save