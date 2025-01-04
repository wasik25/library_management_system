from django.urls import path
from .views import BookListView, BookDetailView, BorrowBookView, ReviewBookView, ReturnBookView, books_list

urlpatterns = [
    path('', books_list, name='books_list'), 
    path('books/', BookListView.as_view(), name='book_list'),  
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/borrow/', BorrowBookView.as_view(), name='borrow_book'),  
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return_book'), 
    path('<int:pk>/review/', ReviewBookView.as_view(), name='review_book'), 
]
