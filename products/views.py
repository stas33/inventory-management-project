from django.shortcuts import render, redirect
from .models import Product
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from invmanagement.authentications import unauthenticated_user, allowed_users
# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'customer'])
def products(request):
    header = 'Available products'
    form = ProductSearchForm(request.POST or None)

    queryset = Product.objects.all()
    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
    }
    if request.method == 'POST':
        queryset = Product.objects.filter(category__icontains=form['category'].value(),
                                          prod_name__icontains=form['prod_name'].value()
                                          )
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "products/list_products.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def create_product(request):
    form = CreateProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product created successfully!')
        return redirect("/products")
    context = {
        "form": form,
        "title": "Add Product",
    }
    return render(request, "products/create_product.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def update_product(request, pk):
    title = "Update product"
    queryset = Product.objects.get(id=pk)
    form = ProductUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('/products')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'products/create_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def delete_product(request, pk):
    queryset = Product.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('/products')
    return render(request, 'products/delete_product.html')