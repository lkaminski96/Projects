from django.urls import path, include

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.BookList.as_view(), name='book-list'),
    path('<int:page>', views.BookList.as_view(), name='paged-book-list'),
    path('add/', views.AddBook.as_view(), name='add-book'),
    path('import/', views.import_books, name='import-books'),
    path('rest/', views.BookRestList.as_view(), name='rest'),
]