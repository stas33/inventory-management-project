from django import forms
from .models import Company
from django.forms import ModelForm

class CompanySearchForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['address', 'postcode']