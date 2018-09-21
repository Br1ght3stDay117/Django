from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Create your models here.

class Movie(models.Model):
    title = models.CharField(blank=True, max_length=100)
    description = models.CharField(blank=True, max_length=300)

    def avg_rating(self):
        sum = 0
        all_ratings = Rating.objects.filter(movie=self)
        for rating in all_ratings:
            sum += rating.stars
        if len(all_ratings) > 0:
            return sum / len(all_ratings)
        else:
            return 0

    def no_of_ratings(self):
        all_ratings = Rating.objects.filter(movie=self)
        return len(all_ratings)


class Rating(models.Model):
    """(Rating movies)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)
