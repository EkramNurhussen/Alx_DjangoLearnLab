# api/urls.py
from django.urls import path
from .views import ListView, CreateView, DetailView, UpdateView, DeleteView

urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),  # List all books
    path('books/create/', CreateView.as_view(), name='book-create'),  # Create a book
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),  # Retrieve a book
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),  # Update a book
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),  # Delete a book
]