from django import forms
from .models import Product
from django.forms import ModelForm


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'prod_name', 'quantity', 'price', 'availability']

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
        fields = ['prod_name', 'quantity', 'availability']