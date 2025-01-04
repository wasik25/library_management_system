from django.shortcuts import render
from django.views.generic import TemplateView
from library.models import Book, Category

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.request.GET.get('category')  
        if category_name:
            context['books'] = Book.objects.filter(categories__name=category_name) 
        else:
            context['books'] = Book.objects.all() 
        context['categories'] = Category.objects.all() 
        context['selected_category'] = category_name 
        return context
