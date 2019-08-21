from django import forms
from .models import Book, Author, IndustryIdentifier

class AuthorForm(forms.ModelForm):
    """
        Class provides/represents form fields using model Author.
    """
    class Meta:
        model = Author
        fields = ['fullName']
        labels = {
            'fullName': 'Author',
        }

class IsbnForm(forms.ModelForm):
    """
        Class provides/represents form fields using model IndustryIdentifier.
    """
    class Meta:
        model = IndustryIdentifier
        fields =[
            'isbn',
            'identifier'
        ]
class BookForm(forms.ModelForm):
    """
        Class provides/represents form fields using model Book.
    """
    class Meta:
        model = Book
        fields = [
            'title',
            'publishedDate',
            'pageCount',
            'language',
            'smallThumbnail',
            'thumbnail'
        ]