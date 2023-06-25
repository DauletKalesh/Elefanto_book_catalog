from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response
from main.models import Genre, Author, Book, Review, Favorite
from main.serializers import GenreSerializer, \
    AuthorSerializer, BookSerializer, ReviewSerializer,\
    BookDetailSerializer, FavoritesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from main.filters import BookFilterSet
# Create your views here.

class BooksViewSet(generics.ListAPIView, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title',)
    filterset_class = BookFilterSet

    def get_queryset(self):
        return Book.objects.prefetch_related('authors', 'genres').all()

class BookAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.prefetch_related('authors', 'genres').all()
    serializer_class = BookDetailSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['is_favorite'] = False if request.user.is_anonymous \
            else instance.is_favorite(request.user)
        return Response(data)

class FavoriteAPIView(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoritesSerializer

    def get_queryset(self):
        return Favorite.objects.select_related('book').filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)