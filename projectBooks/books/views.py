# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages 
from django.shortcuts import render
from django.views import generic, View
from django.db.models import Q
from django.core.paginator import Paginator

# REST Framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

#filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Additional imports
import json, requests
from .models import Book, Author, IndustryIdentifier
from .forms import AuthorForm, IsbnForm, BookForm
from .serializers import BookSerializer

class BookList(generic.ListView): 
    """
        Class which displaying books in Bookstore (possible with additional filters).
    """
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books_list'
    paginate_by = 5
    # filtering & searching
    def get_queryset(self):
        """
            Function for searching and filtering.
        """
        booklist = Book.objects.all()
        query = self.request.GET.get('q')
        option = self.request.GET.get('option')
        published_date = self.request.GET.get('date')
        # date and query filtering & searching
        if published_date and query:
            query = query.strip()
            published_date = published_date.strip()
            if option.lower() == "title":
                booklist = booklist.filter(title__icontains=query, publishedDate__icontains=published_date)
            
            elif option.lower() == "authors":
                given_authors = query.split(',')
                given_authors = [author.strip() for author in given_authors]
                queries = [Q(authors__fullName__icontains=author) & Q(publishedDate__icontains=published_date) 
                           for author in given_authors]
                filter_query = queries.pop()
                for item in queries:
                    filter_query |= item
                booklist = booklist.filter(filter_query)
            
            elif option.lower() == "language":
                booklist = booklist.filter(language__icontains=query, publishedDate__icontains=published_date)
        # query searching
        elif query:
            query = query.strip()
            if option.lower() == "title":
                booklist = booklist.filter(title__icontains=query)
            
            elif option.lower() == "authors":
                given_authors = query.split(',')
                print(given_authors)
                given_authors = [author.strip() for author in given_authors]
                queries = [Q(authors__fullName__icontains=author) for author in given_authors]
                filter_query = queries.pop()               
                for item in queries:
                    filter_query |= item
                booklist = booklist.filter(filter_query)
            
            elif option.lower() == "language":
                booklist = booklist.filter(language__icontains=query)
        # date filtering
        elif published_date:
            published_date = published_date.strip()
            booklist = booklist.filter(publishedDate__icontains=published_date)
        
        return booklist.order_by('id').reverse()


class AddBook(View):
    """
        Class for adding books in Bookstore.
    """
    def get(self, request):
        """
            Function for creating form to add book.
        """
        author_form = AuthorForm(instance=Author())
        book_form = BookForm(instance=Book())
        isbn_forms = [IsbnForm(prefix=str(i), instance=IndustryIdentifier()) for i in range(2)]
        context = {
        'author_form': author_form,
        'book_form': book_form,
        'isbn_forms': isbn_forms,
        }
        return render(request, "books/add_book.html", context)

    def post(self, request):
        """
            Function for sending filled form fields.
        """
        context = {}
        author_form = AuthorForm(request.POST, instance=Author())
        book_form = BookForm(request.POST, instance=Book())
        isbn_forms = [IsbnForm(request.POST, prefix=str(i), instance=IndustryIdentifier()) for i in range(2)]
        # validation of forms
        if (book_form.is_valid() and 
            author_form.is_valid() and 
            all([isbnf.is_valid() for isbnf in isbn_forms])):
            book_to_add = book_form.save()
            # adding authors for book
            author_cleaned_data = author_form.cleaned_data
            authors_string = author_cleaned_data["fullName"]
            authors = authors_string.split(',')           
            for authorName in authors:
                authorName = authorName.strip()               
                if Author.objects.all().filter(fullName=authorName).exists():
                    a = Author.objects.get(fullName=authorName)                
                else:
                    a = Author(fullName=authorName)                
                a.save()
                book_to_add.authors.add(a)
            # adding isbns for book
            for isbnf in isbn_forms:
                isbn_cleaned_data = isbnf.cleaned_data
                isbn_to_add = isbn_cleaned_data["isbn"]
                identifier_to_add = isbn_cleaned_data["identifier"]                
                if IndustryIdentifier.objects.all().filter(isbn=isbn_cleaned_data["isbn"], identifier=isbn_cleaned_data["identifier"]).exists():
                    related_identifier = IndustryIdentifier.objects.get(isbn=isbn_cleaned_data["isbn"], identifier=isbn_cleaned_data["identifier"])
                else:
                    related_identifier = IndustryIdentifier(isbn=isbn_cleaned_data["isbn"], identifier=isbn_cleaned_data["identifier"])               
                related_identifier.save()
                book_to_add.industryIdentifiers.add(related_identifier)
            # final steps after successful add
            messages.success(request, "Sucessfully added book.")
            return HttpResponseRedirect('/books/')
        # re rendering forms in case when any of form is invalid
        context = {
        'author_form': author_form,
        'book_form': book_form,
        'isbn_forms': isbn_forms,
        }
        return render(request, "books/add_book.html", context)


def import_books(request):
    """
        Function for importing books.
    """
    query = request.POST
    if query:
        search_query = query['search'].strip()
        title = "intitle:" + query['title'].strip()
        author = "inauthor:" + query['author'].strip()
        isbn = "isbn:" + query['isbn'].strip()
        # possible cases with provided query
        if query['author'] and query['title'] and query['isbn']:
            load_data(search_query + '+' + author + '+' + title + '+' + isbn)

        elif query['author'] and query['title']:
            load_data(search_query + '+' + author + '+' + title)

        elif query['author'] and query['isbn']:
            load_data(search_query + '+' + author + '+' + isbn)

        elif query['title'] and query['isbn']:
            load_data(search_query + '+' + title + '+' + isbn)

        elif query['author']:
            load_data(search_query + '+' + author)

        elif query['title']:
            load_data(search_query + '+' + title)

        elif query['isbn']:
            load_data(search_query + '+' + isbn)

        else:
            load_data(search_query)
        # final steps after successful import
        messages.success(request, "Sucessfully imported books")
        return HttpResponseRedirect('/books/')
    # re rendering when query wasn't given
    return render(request, "books/import_books.html")


def load_data(q):
    """
        Function which loads JSON data from url.
        parameters:
        q - given query from import view.
    """

    # getting data from URL and parsing JSON
    webURL = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + q)
    data = webURL.text 
    jsonData = json.loads(data, encoding='UTF-8')

    # adding new books
    for element in jsonData["items"]:
        b = Book(title="No title" if 'title' not in element["volumeInfo"] else element["volumeInfo"]["title"],
                 publishedDate="No date" if 'publishedDate' not in element["volumeInfo"] else element["volumeInfo"]["publishedDate"],
                 pageCount=0 if 'pageCount' not in element["volumeInfo"] else element["volumeInfo"]["pageCount"],
                 language="No language" if 'language' not in element["volumeInfo"] else element["volumeInfo"]["language"],
                 smallThumbnail="No smallThumbnail" if 'smallThumbnail' not in element["volumeInfo"]["imageLinks"] else element["volumeInfo"]["imageLinks"]["smallThumbnail"],
                 thumbnail="No thumbnail" if 'thumbnail' not in element["volumeInfo"]["imageLinks"] else element["volumeInfo"]["imageLinks"]["thumbnail"])
        b.save()       
        if 'authors' not in element['volumeInfo']:           
            if Author.objects.all().filter(fullName="No authors").exists():
                a = Author.objects.get(fullName="No authors")
            else:
                a = Author(fullName="No authors")
            a.save()
            b.authors.add(a)
        else:
            for authorName in element["volumeInfo"]["authors"]:
                if Author.objects.all().filter(fullName=authorName).exists():
                    a = Author.objects.get(fullName=authorName)
                else:
                    a = Author(fullName=authorName)
                a.save()
                b.authors.add(a)
        if 'industryIdentifiers' not in element['volumeInfo']:
            if IndustryIdentifier.objects.all().filter(isbn="No ISBN", identifier="No ISBN").exists():
                i = IndustryIdentifier.objects.get(isbn="No ISBN", identifier="No ISBN")
            else:
                i = IndustryIdentifier(isbn="No ISBN", identifier="No ISBN")
            i.save()
            b.industryIdentifiers.add(i)
        else:
            for identifiers in element["volumeInfo"]["industryIdentifiers"]:
                if IndustryIdentifier.objects.all().filter(isbn=identifiers["type"], identifier=identifiers["identifier"]).exists():
                    i = IndustryIdentifier.objects.get(isbn=identifiers["type"], identifier=identifiers["identifier"])
                else:
                    i = IndustryIdentifier(isbn=identifiers["type"], identifier=identifiers["identifier"])
                i.save()
                b.industryIdentifiers.add(i)


class BookRestList(generics.ListAPIView):
    """
        List all books (with possible searching & filtering).
    """ 
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # filters and searching
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['authors__fullName', 'title', 'language']
    filterset_fields = ['publishedDate']
        