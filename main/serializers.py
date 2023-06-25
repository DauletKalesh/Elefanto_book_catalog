from rest_framework import serializers
from main.models import Genre, Author, Book, Review, Favorite

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Review
        fields = ('user', 'username', 'rating', 'text')

class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    authors = AuthorSerializer()
    average_rating = serializers.FloatField(read_only=True, source='get_average_rating')

    class Meta:
        model = Book
        fields = ('id','title', 'genres', 'authors', 'average_rating')


class BookDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    authors = AuthorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True, source='get_average_rating')

    class Meta:
        model = Book
        fields = ('id','title', 'genres', 'authors',
                  'reviews', 'publication_date', 'average_rating')

class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'book')
