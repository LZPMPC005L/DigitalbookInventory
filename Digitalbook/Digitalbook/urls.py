from django.contrib import admin
from django.urls import path
from book.views import add_book
from book.views import add_author
from book.views import get_authors
from book.views import get_books
from book.views import BookView
from book.views import delete_book
from book.views import search_books
from book.views import sort_books
from book.views import update_book
from book.views import add_multiple_books
from book.views import delete_multiple_books

urlpatterns = [
    path("admin/", admin.site.urls),
    path('add_book/', add_book, name='add_book'),
    path('add_author/', add_book, name='add_author'),
    path('get_authors/', get_authors, name='get_authors'),
    path('get_books/', get_books, name='get_books'),
    path('bookview/',BookView.as_view(), name='book-view'),
    path('delete_book/',delete_book, name='delete_book'),
    path('search_books/', search_books, name='search_books'),
    path('sort_books/', sort_books, name='sort_books'),
    path('update_book/<int:pk>/', update_book, name='update_book'),
    path('add_multiple_books/', add_multiple_books, name='add_multiple_books'),
    path('delete_multiple_books/', delete_multiple_books, name='delete_multiple_books'),

]

