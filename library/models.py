from django.db import models
from accounts.models import UserAccount
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='books') 
    borrow_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.title

class Borrow(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def return_book(self):
        if not self.returned:
            self.user.balance += self.book.borrow_price
            self.user.save()
            self.returned = True
            self.save()
    
    def __str__(self):
        return f"{self.user.user.username} borrowed {self.book.title}"



class Review(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.user.username} for {self.book.title}"