from django.contrib import admin
from .models import Category, Book, Borrow, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    ordering = ('name',) 

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'borrow_price')
    search_fields = ['title']
    ordering = ('title',)
    list_filter = ('categories',) 

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned')
    list_filter = ('returned', 'borrowed_at')
    ordering = ('-borrowed_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',) 
