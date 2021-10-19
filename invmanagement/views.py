from django.shortcuts import render, redirect
from .models import *
from .forms import CreateProductForm, ProductSearchForm, ProductUpdateForm, CreateUserForm
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    title = "Welcome: This is the home page!"
    context = {
        "title": title,
        #"form": form,
    }
    return render(request, "home.html", context)


@login_required(login_url='login')
def products(request):
    header = 'List of products'
    update = "Update"
    form = ProductSearchForm(request.POST or None)

    queryset = Product.objects.all()
    context = {
        "update": update,
        "form": form,
        "header": header,
        "queryset": queryset,
    }
    if request.method == 'POST':
        queryset = Product.objects.filter(category__icontains=form['category'].value(),
                                        prod_name__icontains=form['prod_name'].value()
                                        )
        context = {
            "update": update,
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "list_products.html", context)


@login_required(login_url='login')
def create_product(request):
    form = CreateProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product created successfully!')
        return redirect("/products")
    context = {
        "form": form,
        "title": "Create Product",
    }
    return render(request, "create_product.html", context)


@login_required(login_url='login')
def update_product(request, pk):
    queryset = Product.objects.get(id=pk)
    form = ProductUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('/products')
    context = {
        'form':form
    }
    return render(request, 'create_product.html', context)


@login_required(login_url='login')
def delete_product(request, pk):
    queryset = Product.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('/products')
    return render(request, 'delete_product.html')