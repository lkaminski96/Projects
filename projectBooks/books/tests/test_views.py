from django.test import TestCase, Client
from django.urls import reverse
from books.models import Author, Book, IndustryIdentifier
import json
from rest_framework.test import APIClient, RequestsClient
class TestViews(TestCase):
    """
        Class for testing views.
    """
    
    def setUp(self):
        """
            Startup configuration for every test.
        """
        self.client = Client()
        self.book_list_url = reverse('books:book-list')
        self.paged_book_list_url = reverse('books:paged-book-list', args=[1])
        self.add_book_url = reverse('books:add-book')
        self.import_books_url = reverse('books:import-books')
        self.book_list_rest_url = reverse('books:rest')

    def test_book_list_view_GET(self):
        response = self.client.get(self.book_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertEquals(Book.objects.count(), 0)

        author = Author(
            fullName='Author'
        )
        author.save()
        isbn = IndustryIdentifier(
            isbn='ISBN_10',
            identifier='1234567890'
        )
        isbn.save()
        book = Book(
            title='Title',
            publishedDate='2019',
            pageCount=0,
            language='en',
            smallThumbnail='http://books.google.com/books/content?id=hFfhrCWiLSMC&printsec=frontcover&img=1&zoom=5&source=gbs_api',
            thumbnail='http://books.google.com/books/content?id=hFfhrCWiLSMC&printsec=frontcover&img=1&zoom=1&source=gbs_api'
        )
        book.save()
        book.authors.add(author)
        book.industryIdentifiers.add(isbn)
        
        self.assertEquals(Book.objects.count(), 1)
    
    def test_paged_book_list_view_GET(self):
        response = self.client.get(self.paged_book_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
    
    def test_add_book_GET(self):
        response = self.client.get(self.add_book_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/add_book.html')

    def test_add_book_POST(self):
        self.assertEquals(Book.objects.all().count(), 0)
        response = self.client.post(self.add_book_url, data={
            'fullName': 'Author',
            'title': 'Title',
            'publishedDate': '2019',
            'pageCount': 0,
            'language': 'en',
            'smallThumbnail': 'http://books.google.com/books/content?id=hFfhrCWiLSMC&printsec=frontcover&img=1&zoom=5&source=gbs_api',
            'thumbnail': 'http://books.google.com/books/content?id=hFfhrCWiLSMC&printsec=frontcover&img=1&zoom=1&source=gbs_api',
            'isbn': 'ISBN_10',
            'identifier': '1234567890',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Book.objects.all().count(), 1)

    def test_import_books_POST_with_search_query(self):
        self.assertEquals(Book.objects.all().count(), 0)
        response = self.client.post(self.import_books_url, data={
            'search': 'Hobbit',
            'title': '',
            'author': '',
            'isbn': '',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Book.objects.all().count(), 10)
    
    def test_import_books_POST_with_no_search_query(self):
        response = self.client.post(self.import_books_url, data=None)
        self.assertTemplateUsed(response, 'books/import_books.html')


    def test_import_books_POST_with_search_query_and_author(self):
        self.assertEquals(Book.objects.all().count(), 0)
        response = self.client.post(self.import_books_url, data={
            'search': 'Hobbit',
            'title': '',
            'author': 'Jim Ware',
            'isbn': '',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Book.objects.all().count(), 3)

    def test_import_books_POST_with_search_query_and_title(self):
        self.assertEquals(Book.objects.all().count(), 0)
        response = self.client.post(self.import_books_url, data={
            'search': 'Hobbit',
            'title': 'Hobbit',
            'author': '',
            'isbn': '',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Book.objects.all().count(), 10)
    
    def test_import_books_POST_with_search_query_and_isbn(self):
        self.assertEquals(Book.objects.all().count(), 0)
        
        response = self.client.post(self.import_books_url, data={
            'search': 'Hobbit',
            'title': '',
            'author': '',
            'isbn': '9780345339683',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Book.objects.all().count(), 4)
    
    def test_book_rest_list_GET(self):
        rest_client = RequestsClient()
        response = rest_client.get('http://localhost:8000/books/rest/')
        
        assert response.status_code == 200

