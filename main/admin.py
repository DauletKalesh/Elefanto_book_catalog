from django.contrib import admin
from main.models import Book, Author, Genre, Review, Favorite
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Favorite)