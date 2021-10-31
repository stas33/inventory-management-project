from django import forms
from .models import Order
from django.forms import ModelForm

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