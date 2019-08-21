from django.test import SimpleTestCase
from django.urls import resolve, reverse
from books.views import BookList, AddBook, import_books, BookRestList

class TestUrls(SimpleTestCase):
    """
        Class for testing urls.
    """
    
    # Testing if provided url uses connected with it view
    def test_book_list_url(self):
        url = reverse('books:book-list')
        self.assertEquals(resolve(url).func.view_class, BookList)
    
    def test_book_list_paged_url(self):
        url = reverse('books:paged-book-list', args=[1])
        self.assertEquals(resolve(url).func.view_class, BookList)

    def test_add_url(self):
        url = reverse('books:add-book')
        self.assertEquals(resolve(url).func.view_class, AddBook)

    def test_import_url(self):
        url = reverse('books:import-books')
        self.assertEquals(resolve(url).func, import_books)

    def test_book_rest_url(self):
        url = reverse('books:rest')
        self.assertEquals(resolve(url).func.view_class, BookRestList)