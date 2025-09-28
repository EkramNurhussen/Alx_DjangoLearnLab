# api/test_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Author, Book
from api.serializers import BookSerializer

class BookAPITests(APITestCase):
    def setUp(self):
        """Set up test data, client, and authenticated user."""
        self.author = Author.objects.create(name="Jane Doe")
        self.book = Book.objects.create(title="Test Book", publication_year=2020, author=self.author)
        self.book_data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_list_books_unauthenticated(self):
        """Test listing books without authentication (read-only, status 200)."""
        self.client.logout()
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_create_book_authenticated(self):
        """Test creating a book with authentication (status 201)."""
        response = self.client.post(reverse('book-create'), self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Book')

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (status 403)."""
        self.client.logout()
        response = self.client.post(reverse('book-create'), self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book_unauthenticated(self):
        """Test retrieving a book without authentication (read-only, status 200)."""
        self.client.logout()
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book_authenticated(self):
        """Test updating a book with authentication (status 200)."""
        updated_data = {'title': 'Updated Book', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.put(reverse('book-update', kwargs={'pk': self.book.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        self.assertEqual(self.book.publication_year, 2022)

    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication (status 403)."""
        self.client.logout()
        updated_data = {'title': 'Updated Book', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.put(reverse('book-update', kwargs={'pk': self.book.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication (status 204)."""
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication (status 403)."""
        self.client.logout()
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_title(self):
        """Test filtering books by title (status 200)."""
        response = self.client.get(reverse('book-list') + '?title=Test%20Book')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication_year (status 200)."""
        response = self.client.get(reverse('book-list') + '?publication_year=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2020)

    def test_filter_books_by_author(self):
        """Test filtering books by author (status 200)."""
        response = self.client.get(reverse('book-list') + f'?author={self.author.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author.id)

    def test_search_books_by_title(self):
        """Test searching books by title (status 200)."""
        response = self.client.get(reverse('book-list') + '?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_search_books_by_author_name(self):
        """Test searching books by author name (status 200)."""
        response = self.client.get(reverse('book-list') + '?search=Jane')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author.id)

    def test_ordering_books_by_publication_year(self):
        """Test ordering books by publication_year descending (status 200)."""
        Book.objects.create(title="Another Book", publication_year=2019, author=self.author)
        response = self.client.get(reverse('book-list') + '?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['publication_year'], 2020)
        self.assertEqual(response.data[1]['publication_year'], 2019)

    def test_ordering_books_by_title(self):
        """Test ordering books by title ascending (status 200)."""
        Book.objects.create(title="Another Book", publication_year=2019, author=self.author)
        response = self.client.get(reverse('book-list') + '?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Another Book')
        self.assertEqual(response.data[1]['title'], 'Test Book')