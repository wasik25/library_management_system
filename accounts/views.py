from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import UserRegistrationForm, DepositForm
from .models import UserAccount
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from library.models import Borrow

@login_required
def profile_view(request):
    user_account = request.user.account
    borrow_history = Borrow.objects.filter(user=user_account)
    
    context = {
        'user_account': user_account,
        'borrow_history': borrow_history,
    }
    return render(request, 'accounts/profile.html', context)

class UserRegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class DepositView(FormView):
    template_name = 'accounts/deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        account, created = UserAccount.objects.get_or_create(user=user)
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()

        messages.success(self.request, f"Successfully deposited {amount} to your account!")
        return super().form_valid(form)

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'