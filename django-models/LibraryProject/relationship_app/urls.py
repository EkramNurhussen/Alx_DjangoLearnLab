from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='books/', permanent=False)),  # Redirect root to books/
    path('books/', views.book_list, name='book_list'),
    path('library/detail/<int:id>/', views.LibraryDetailView.as_view(), name='library_detail'),
]