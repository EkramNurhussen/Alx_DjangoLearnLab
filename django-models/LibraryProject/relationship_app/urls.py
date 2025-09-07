from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import book_list, LibraryDetailView
urlpatterns = [
    path('', RedirectView.as_view(url='books/', permanent=False)),  # Redirect root to books/
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]
