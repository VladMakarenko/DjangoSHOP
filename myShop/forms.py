from django import forms
from django.contrib.auth.forms import UserCreationForm

from myShop.models import MyUser, Purchase, Return


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    wallet = forms.DecimalField(initial=10_000, widget=forms.HiddenInput)

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'wallet')


class PurchaseCreateForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=1, widget=forms.NumberInput(attrs={'min': 1}))

    class Meta:
        model = Purchase
        fields = ['quantity']


class ReturnCreateForm(forms.ModelForm):
    purchase = forms.ModelChoiceField(queryset=Purchase.objects.all(), required=False, widget=forms.HiddenInput)

    class Meta:
        model = Return
        fields = ['purchase']
