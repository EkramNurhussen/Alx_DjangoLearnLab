# api/models.py
from django.db import models

# Author model to store author information
class Author(models.Model):
    name = models.CharField(max_length=100)  # Author's name, max length 100 characters

    def __str__(self):
        return self.name

# Book model with a foreign key to Author
class Book(models.Model):
    title = models.CharField(max_length=200)  # Book title, max length 200 characters
    publication_year = models.IntegerField()  # Year of publication
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  # One-to-many relationship with Author

    def __str__(self):
        return self.title