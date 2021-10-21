from django import forms
from .models import Product, Order, STATUS
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'prod_name', 'quantity']

    #def clean_category(self):
     #   category = self.cleaned_data.get('category')
     #   if not category:
      #      raise forms.ValidationError('This field is required')

        # avoid duplicating categories with the same name
        #for instance in Product.objects.all():
        #    if instance.category == category:
        #        raise forms.ValidationError(category + ' is already created')
        #return category

    def clean_prod_name(self):
        prod_name = self.cleaned_data.get('prod_name')
        if not prod_name:
            raise forms.ValidationError('This field is required')
        return prod_name

class ProductSearchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'prod_name']

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'prod_name', 'quantity']

class OrderSearchForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if not status:
            raise forms.ValidationError('This field is required')
        return status

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class CustomerSearchForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']