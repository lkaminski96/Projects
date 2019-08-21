from django.db import models

class Author(models.Model):
    """
        Class represents table author in database.
    """
    fullName = models.CharField(max_length=200)
    
    def __str__(self):
        """
            Function returns easier to read object representation.
        """
        return self.fullName

class IndustryIdentifier(models.Model):
    """
        Class represents table industry identifiers in database.
    """
    isbn = models.CharField(max_length=10, blank=True)
    identifier = models.CharField(max_length=30, blank=True)

    def __str__(self):
        """
            Function returns easier to read object representation.
        """
        return self.isbn + ' ' + self.identifier
        
class Book(models.Model):
    """
        Class represents table book in database.
    """
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    publishedDate = models.CharField(max_length=15)
    industryIdentifiers = models.ManyToManyField(IndustryIdentifier)
    pageCount = models.IntegerField(default=0)
    language = models.CharField(max_length=20)
    smallThumbnail = models.URLField(max_length=200)
    thumbnail = models.URLField(max_length=200)

    def __str__(self):
        """
            Function returns easier to read object representation.
        """
        return self.title



