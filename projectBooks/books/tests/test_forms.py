from django.test import SimpleTestCase
from books.forms import AuthorForm, BookForm, IsbnForm

class TestForms(SimpleTestCase):
    """
        Class for testing forms.
    """
    # Author form
    def test_author_form_is_valid(self):
        form = AuthorForm(data={
            'fullName': 'Author'
        })
        
        self.assertTrue(form.is_valid())
    
    def test_author_form_is_invalid(self):
        form = AuthorForm(data={})
        
        self.assertFalse(form.is_valid())

    # Book form
    def test_book_form_is_valid(self):
        form = BookForm(data={
            'title': 'Title',
            'publishedDate': '2019',
            'pageCount': '0',
            'language': 'en',
            'smallThumbnail': 'http://books.google.com/books/content?id=hFfhrCWiLSMC&printsec=frontcover&img=1&zoom=5&source=gbs_api',
            'thumbnail': 'http://books.google.com/books/content?id=hFfhrCWiLSMC&printsec=frontcover&img=1&zoom=1&source=gbs_api'
        })
        
        self.assertTrue(form.is_valid())
    
    def test_book_form_is_invalid(self):
        form = BookForm(data={})
        
        self.assertFalse(form.is_valid())

    # ISBN form
    def test_isbn_form_is_valid(self):
        form = IsbnForm(data={
            'isbn': 'ISBN_10',
            'identifier': '1234567890'
        })
        
        self.assertTrue(form.is_valid())