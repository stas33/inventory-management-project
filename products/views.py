from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from invmanagement.authentications import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
from .filters import ProductSearchFilter
from dal import autocomplete


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def categories(request):
    header = 'Select a category'
    queryset = Category.objects.all()

    context = {
        "header": header,
        "queryset": queryset,
    }
    return render(request, "products/categories.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def product_list(request, pk):
    category = Category.objects.get(id=pk)
    header = f"Products of category {category.name}"
    queryset = Product.objects.filter(category__id=pk).order_by('id')
    for prod in queryset:
        if prod.quantity == 0:
            messages.warning(request, f"The quantity of product {prod.prod_name} is zero!")

    filter = ProductSearchFilter(request.GET, queryset=queryset)
    title = "Advanced Search"

    product_paginator = Paginator(filter.qs, 2)
    page = request.GET.get('page')
    prods = product_paginator.get_page(page)

    context = {
        'header': header,
        'queryset': queryset,
        'prods': prods,
        'filter': filter,
        'title': title,
    }
    return render(request, 'products/product_list.html', context)


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
    categories = Category.objects.all()
    queryset = Product.objects.get(id=pk)
    categ = Product.objects.get(id=pk, category__id__in=categories)
    id = categ.category.id
    form = ProductUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(f"/products/categories/{id}")
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'products/create_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def delete_product(request, pk):
    categories = Category.objects.all()
    categ = Product.objects.get(id=pk, category__id__in=categories)
    categid = categ.category.id
    if request.method == 'POST':

        messages.success(request, 'Product deleted successfully!')
        return redirect(f"/products/categories/{categid}")
    return render(request, 'products/delete_product.html')
