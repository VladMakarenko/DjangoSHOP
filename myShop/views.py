from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from myShop.forms import UserCreateForm, PurchaseCreateForm, ReturnCreateForm
from myShop.models import Product, Purchase, Return


class HomePage(ListView):
    model = Product
    template_name = 'home.html'
    extra_context = {'form': PurchaseCreateForm}
    paginate_by = 3


def product_detail(request, pk):
    try:
        product_id = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404('Ошибочка')

    return render(request, 'product_detail.html',
                  context={'product': product_id, })


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


class ProductCreateView(CreateView):
    model = Product
    fields = ['product_name', 'image', 'description', 'price', 'quantity']
    template_name = 'add_product.html'
    success_url = reverse_lazy('add_product')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['product_name', 'image', 'description', 'price', 'quantity']
    template_name = 'update_product.html'
    success_url = reverse_lazy('home')


class PurchaseListView(ListView):
    login_url = reverse_lazy('login')
    model = Purchase
    template_name = 'purchase.html'
    extra_context = {'form': ReturnCreateForm}
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Purchase.objects.filter(customer=self.request.user)
            return queryset
        queryset = Purchase.objects.all()
        return queryset


class PurchaseCreateView(CreateView):
    login_url = reverse_lazy('login')
    form_class = PurchaseCreateForm
    template_name = 'home.html'
    success_url = reverse_lazy('purchases')

    def form_valid(self, form):
        obj = form.save(commit=False)
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        customer = self.request.user
        ordered_quantity = int(self.request.POST['quantity'])
        if ordered_quantity > product.quantity:
            messages.error(self.request, 'Not enough goods in stock')
            return HttpResponseRedirect('/')
        purchase_amount = product.price * ordered_quantity
        if purchase_amount > customer.wallet:
            messages.error(self.request, 'Not enough funds to make a purchase')
            return HttpResponseRedirect('/')
        obj.product = product
        obj.customer = customer
        product.quantity -= ordered_quantity
        customer.wallet -= purchase_amount

        with transaction.atomic():
            obj.save()
            product.save()
            customer.save()

        return super().form_valid(form)


class ReturnListView(ListView):
    login_url = reverse_lazy('login')
    model = Return
    template_name = 'return_purchase.html'
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Return.objects.filter(purchase__customer=self.request.user)
            return queryset
        queryset = Return.objects.all()
        return queryset


class ReturnCreateView(CreateView):
    login_url = reverse_lazy('login')
    form_class = ReturnCreateForm
    template_name = 'purchase.html'
    success_url = reverse_lazy('returns')

    def form_valid(self, form, RETURN_TIME_LIMIT=60 * 3):
        obj = form.save(commit=False)
        purchase_id = self.kwargs.get('pk')
        purchase = Purchase.objects.get(id=purchase_id)
        check_time_period = timezone.now() - purchase.date
        if check_time_period.seconds > RETURN_TIME_LIMIT:
            messages.error(self.request, 'Return time has expired')
            return HttpResponseRedirect('/purchases')
        obj.purchase = purchase
        obj.save()
        return super().form_valid(form)


class ReturnDeleteView(DeleteView):
    model = Return
    success_url = reverse_lazy('returns')


class PurchaseDeleteView(DeleteView):
    model = Purchase
    success_url = reverse_lazy('returns')

    def form_valid(self, form):
        purchase = self.get_object()
        customer = purchase.customer
        product = purchase.product
        customer.deposit += purchase.purchase_amount
        product.quantity += purchase.quantity

        with transaction.atomic():
            customer.save()
            product.save()
            purchase.delete()
        return HttpResponseRedirect(self.success_url)
