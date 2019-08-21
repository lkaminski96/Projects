from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
        Class represents book as JSON object.
    """
    authors = serializers.StringRelatedField(many=True, read_only=True)
    industryIdentifiers = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
            'publishedDate',
            'industryIdentifiers',
            'pageCount',
            'language',
            'smallThumbnail',
            'thumbnail'
        )