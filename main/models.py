from django.db import models
from django.db.models import Avg

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    authors = models.ForeignKey(
        'Author', on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    genres = models.ManyToManyField(
        'Genre', null=True, blank=True, related_name='books')
    
    @property
    def get_average_rating(self):
        return self.reviews.aggregate(avg_rating=Avg('rating')).get('avg_rating', 0)
    
    def is_favorite(self, user):
        if Favorite.objects.filter(user=user, book=self).first():
            return True
        return False

class Genre(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)


class Author(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)


class UniqueUserBook(models.Model):
    user = models.ForeignKey('custom_auth.MainUser', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], 
                                    name='%(app_label)s_%(class)s_unique_user_book')
        ]

class Review(UniqueUserBook):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    text = models.TextField()

class Favorite(UniqueUserBook):
    user = models.ForeignKey('custom_auth.MainUser', 
                             on_delete=models.CASCADE, related_name='favorites')
    added_day = models.DateField(null=True, blank=True, auto_now=True)
