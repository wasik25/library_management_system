from django import forms
from .models import Review, Book, Category

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'image', 'borrow_price', 'categories']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(),  
            'borrow_price': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Enter Book Title:',
            'image': 'Select an Image:',
            'categories': 'Select Categories:',
            'borrow_price': 'Enter a Price:',
            'description': 'Enter a Description:',
        }
