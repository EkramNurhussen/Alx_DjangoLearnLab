```python
# api/serializers.py
from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# Serializer for the Book model to handle all fields with custom validation
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']  # Serialize all fields of Book model

    def validate_publication_year(self, value):
        """
        Validate that the publication_year is not in the future.
        Raises serializers.ValidationError if the year is invalid.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Serializer for the Author model with nested BookSerializer for related books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serializer to include all related books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include name and related books