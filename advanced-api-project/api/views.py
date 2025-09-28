# api/views.py
from rest_framework import generics
from rest_framework import filters  # Import for SearchFilter and OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as django_filters  # Import for DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# ListView: Handles listing all books with filtering, searching, and ordering
class ListView(generics.ListAPIView):
    """
    View to retrieve a list of all books.
    Supports filtering by title, publication_year, and author using DjangoFilterBackend.
    Supports searching by title and author name using SearchFilter.
    Supports ordering by title and publication_year using OrderingFilter.
    Allows read-only access for unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author']  # Fields for filtering
    search_fields = ['title', 'author__name']  # Fields for searching
    ordering_fields = ['title', 'publication_year']  # Fields for ordering
    ordering = ['title']  # Default ordering

# CreateView: Handles creating a new book
class CreateView(generics.CreateAPIView):
    """
    View to create a new book.
    Requires authentication for creation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Validate and save the book data."""
        serializer.save()

# DetailView: Handles retrieving a single book by ID
class DetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID.
    Allows read-only access for unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# UpdateView: Handles updating an existing book
class UpdateView(generics.UpdateAPIView):
    """
    View to update an existing book by ID.
    Requires authentication for updates.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Validate and save the updated book data."""
        serializer.save()

# DeleteView: Handles deleting a book
class DeleteView(generics.DestroyAPIView):
    """
    View to delete a book by ID.
    Requires authentication for deletion.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]