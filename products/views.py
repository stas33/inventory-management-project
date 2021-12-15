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
# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def categories(request):
    header = 'Select a category'
    queryset = Category.objects.all()
    # pc = Product.objects.filter(category__id='1')
    # pc_count = pc.count()
    context = {
        "header": header,
        "queryset": queryset,
        # "pc_count": pc_count
    }
    return render(request, "products/categories.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def product_list(request, pk):
    category = Category.objects.get(id=pk)
    header = f"Products of category {category.name}"
    queryset = Product.objects.filter(category__id=pk)

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