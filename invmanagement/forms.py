from django import forms
from .models import Product, Order, STATUS, Company, Employee
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models import Q


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ActivateUserForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.filter(Q(name__contains='employee') | Q(name__contains='manager')), required=True)
    class Meta:
        model = User
        fields = ['group']

class ChooseCompanyForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Company.objects.all())
    class Meta:
        model = Company
        fields = ['name']

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'prod_name', 'quantity', 'price']

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
    email = forms.CharField(required=True, max_length=30)
    class Meta:
        model = User
        fields = ['email']

class EmployeeSearchForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=20)
    class Meta:
        model = User
        fields = ['username']

#class CreateEmployeeForm1(forms.ModelForm):
#    class Meta:
#        model = User
#        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class CreateEmployeeForm2(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['company']

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CompanySearchForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['address', 'postcode']