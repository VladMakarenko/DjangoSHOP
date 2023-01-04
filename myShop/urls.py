from django.contrib import admin
from django.urls import path
from django.contrib.auth import views

from .views import UserCreateView, HomePage, product_detail, ProductCreateView, ProductUpdateView, PurchaseListView, \
    ReturnCreateView, ReturnListView, PurchaseDeleteView, ReturnDeleteView, PurchaseCreateView

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('product/<int:pk>', product_detail, name='product_detail'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add-product/', ProductCreateView.as_view(), name='add_product'),
    path('update-product/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('add-purchase/<int:pk>', PurchaseCreateView.as_view(), name='add_purchase'),
    path('add-return/<int:pk>', ReturnCreateView.as_view(), name='add_return'),
    path('returns/', ReturnListView.as_view(), name='returns'),
    path('delete-return/<int:pk>', ReturnDeleteView.as_view(), name='delete_return'),
    path('delete-purchase/<int:pk>', PurchaseDeleteView.as_view(), name='delete_purchase'),

]
