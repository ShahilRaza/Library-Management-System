from django.urls import path
from .views import register_user,login_user,read_book,update_book,delete_book, create_book,filter_books,count_books_by_genre,recent_books,books_by_author_sorted


urlpatterns = [
    path('users/register', register_user, name='register_user'),
    path('users/login/', login_user , name='login_user'),
    path('create/books/', create_book, name='create_book'),
    path('get/books/<int:id>', read_book, name='read_book'),
    path('update/books/<int:id>', update_book, name='update_book'),
    path('delete/books/<int:id>', delete_book, name='delete_book'),
    path('filter/books/', filter_books, name='filter_books'),
    path('count/books/genre/<str:genre>/', count_books_by_genre, name='count_books_by_genre'),
    path('recent/books/', recent_books, name='recent_books'),
    path('books/author/<str:author>/', books_by_author_sorted, name='books_by_author_sorted'),
]