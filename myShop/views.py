from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from myShop.forms import UserCreateForm, PurchaseCreateForm
from myShop.models import Product


class HomePage(ListView):
    model = Product
    template_name = 'home.html'
    extra_context = {'form': PurchaseCreateForm}
    paginate_by = 2


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid
