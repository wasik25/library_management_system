from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Book, Category, Borrow
from .forms import ReviewForm
from django.views import View
from django.utils import timezone
from library.models import Borrow

def books_list(request):
    category_name = request.GET.get('category')

    if category_name is None:
        books = Book.objects.all()  
    else:
        books = Book.objects.filter(categories__name=category_name)  

    categories = Category.objects.all() 
    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_name, 
    }
    return render(request, 'library/books_list.html', context) 


class BookListView(TemplateView):
    template_name = "library/book_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        context['books'] = Book.objects.filter(category_id=category_id) if category_id else Book.objects.all()
        context['categories'] = Category.objects.all()
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = "library/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        if self.request.user.is_authenticated:
            context['user_borrowed'] = Borrow.objects.filter(
                user=self.request.user.account, book=self.object, returned=False
            ).exists()
        else:
            context['user_borrowed'] = False
        return context

class BorrowBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        account = request.user.account

        if account.balance >= book.borrow_price:
            account.balance -= book.borrow_price
            account.save()

            Borrow.objects.create(user=account, book=book)

            messages.success(request, f"Successfully borrowed '{book.title}'.")
            return redirect('book_detail', pk=book.pk)

        messages.error(request, "Insufficient balance to borrow this book.")
        return redirect('book_detail', pk=book.pk)

class ReviewBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user.account
            review.book = book
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('book_detail', pk=book.pk)

        messages.error(request, "There was an error with your review submission.")
        return render(request, 'library/book_detail.html', {'object': book, 'review_form': form})

class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        borrow = get_object_or_404(Borrow, pk=pk, user=request.user.account)
        if not borrow.returned:
            borrow.return_book()
            messages.success(request, f"'{borrow.book.title}' has been successfully returned!")
        else:
            messages.error(request, f"'{borrow.book.title}' has already been returned.")
        return redirect('profile')