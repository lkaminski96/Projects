from django.contrib import admin

from .models import Book, Author, IndustryIdentifier
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(IndustryIdentifier)
