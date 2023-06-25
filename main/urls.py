from django.urls import path
from main.views import BooksViewSet, BookAPIView, FavoriteAPIView

urlpatterns = [
    path('books/', BooksViewSet.as_view({'get': 'list'})),
    path('books/<int:pk>', BookAPIView.as_view()),
    path('favorites/', FavoriteAPIView.as_view()),

]