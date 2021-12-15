from django.shortcuts import render, redirect
from .models import *
from .forms import *
from companies.models import Company
from products.models import *
from orders.models import Order
from products.filters import ProductCustomerFilter
from .filters import *
from companies.forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .authentications import unauthenticated_user, allowed_users
from django.core.paginator import Paginator


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    form1 = ActivateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form1 = ActivateUserForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            reg_user = get_user_model().objects.get(username=username)
            reg_user.is_active = False
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            group = form1['group'].value()
            if group == '3':
                submitted_group = Group.objects.get(id=5)
                reg_user.groups.add(submitted_group)
                reg_user.save()
            if group == '2':
                submitted_group = Group.objects.get(id=6)
                reg_user.groups.add(submitted_group)
                reg_user.save()

            messages.success(request, 'Register request for {' + username + '} has been sent!')
            return redirect('login')

    context = {'form': form,
               'form1': form1
               }
    return render(request, 'auth/register.html', context)


@unauthenticated_user
def registerCustomerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
                name=username,
                email=email
            )

            messages.success(request, 'Account was created for customer: ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'auth/register-customer.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group = None
            if user.groups.exists():
                group = request.user.groups.all()[0].name
                # if user.is_super:
                #    return redirect('homePage_customers')
            # if user.groups.all()[0].name == 'customer':
            #     redirect('choose_categories')
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'auth/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def inactive_employees(request):
    header = 'Pending employee requests'
    # form = CustomerSearchForm(request.POST or None)
    # group = request.user.groups.all().name == "customer"
    queryset = User.objects.filter(is_active=False, groups__name='pending employee')
    context = {
        # "form": form,
        "header": header,
        "queryset": queryset,
    }

    return render(request, "users/inactive_employees.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def inactive_managers(request):
    header = 'Pending manager requests'
    # form = CustomerSearchForm(request.POST or None)
    # group = request.user.groups.all().name == "customer"
    queryset = User.objects.filter(is_active=False, groups__name='pending manager')
    context = {
        # "form": form,
        "header": header,
        "queryset": queryset,
    }

    return render(request, "users/inactive_managers.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def activate_user(request, pk):
    title = "Choose Company"
    queryset = User.objects.get(id=pk)
    queryset1 = Company.objects.all()
    # form = ActivateUserForm(instance=queryset)
    form1 = ChooseCompanyForm(request.POST or None)
    if request.method == 'POST':
        # form = ActivateUserForm(request.POST, instance=queryset)
        if form1.is_valid():
            queryset.is_active = True
            # group = form['group'].value()
            group = 'pending employee'.join(map(str, queryset.groups.all()))
            # queryset.groups.add(group)
            # queryset.save()
            # form.save()
            if group == 'pending employee':
                # form1 = ChooseCompanyForm(request.POST, instance=queryset1)
                activate_group = Group.objects.get(id=3)
                queryset.groups.add(activate_group)
                compid = form1['name'].value()
                employee = Employee(user=User(id=pk), company=Company(id=compid))
                queryset.save()
                employee.save()
                messages.success(request, 'Employee activated successfully!')
                return redirect('/inactive_employees')
            else:
                activate_group = Group.objects.get(id=2)
                queryset.groups.add(activate_group)
                queryset.save()
                messages.success(request, 'Manager activated successfully!')
                return redirect('/inactive_managers')
    context = {
        'title': title,
        # 'form': form,
        'form1': form1
    }
    return render(request, 'users/activate_user.html', context)


@login_required(login_url='login')
def home(request):
    title = "Welcome: This is the home page of the inventory management system!"
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter(groups=4)
    customer_count = customer.count()
    employee = User.objects.filter(groups=3)
    employee_count = employee.count()
    company = Company.objects.all()
    company_count = company.count()
    inactive_usr = User.objects.filter(is_active=False)
    inactive_count = inactive_usr.count()
    context = {
        "title": title,
        "product_count": product_count,
        "order_count": order_count,
        "customer_count": customer_count,
        "employee_count": employee_count,
        "company_count": company_count,
        "inactive_count": inactive_count
    }
    return render(request, "home.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def employees(request):
    header = 'Employees list'
    # form = EmployeeSearchForm(request.POST or None)
    # group = request.user.groups.all().name == "customer"
    queryset = User.objects.filter(groups__name='employee')
    filter = EmployeeSearchFilter(request.GET, queryset=queryset)
    queryset = filter.qs
    title = "Advanced Search"

    # queryset = Employee.objects.filter(user__groups__name='employee')
    context = {
        "header": header,
        "title": title,
        "filter": filter,
        "queryset": queryset,
    }
    # if request.method == 'POST':
    #     queryset1 = User.objects.filter(username__icontains=form['username'].value())
    #     # form.fields['customer'].queryset = User.objects.filter()
    #     context = {
    #         "form": form,
    #         "header": header,
    #         "queryset": queryset,
    #     }
    return render(request, "users/list_employees.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def create_employee(request):
    form1 = CreateUserForm(request.POST or None)
    form2 = CreateEmployeeForm2(request.POST or None)
    if form1.is_valid() and form2.is_valid():
        # form.save()
        # user = User.objects.get(username=request.POST.get('username'))
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        createduser = User(username=username, first_name=firstname, last_name=lastname, email=email, password=password2)
        user = form1.save()
        group = Group.objects.get(name='employee')
        user.groups.add(group)

        userid = request.user.id
        companyid = request.POST.get('company')
        # company=request.POST.get('company')
        empcreated = Employee(user=User(id=userid), company=Company(companyid))
        empcreated.save()
        messages.success(request, 'Employee created successfully!')
        return redirect("/employees")
    context = {
        "form1": form1,
        "form2": form2,
        "title1": "Add Employee",
        "title2": "Choose company of employee",
    }
    return render(request, "users/create_employee.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def update_employee(request, pk):
    title = "Update Employee"
    queryset = User.objects.get(id=pk)
    # queryset = Employee.objects.get(id=pk)
    form = EmployeeUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('/employees')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'users/update_employee.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def customers(request):
    header = 'Registered customers'
    #form = CustomerSearchForm(request.POST or None)
    # group = request.user.groups.all().name == "customer"
    queryset = User.objects.filter(groups__name='customer')
    filter = CustomerSearchFilter(request.GET, queryset=queryset)
    queryset = filter.qs
    title = "Advanced Search"
    context = {
        "title": title,
        "filter": filter,
        "header": header,
        "queryset": queryset,
    }

    # if request.method == 'POST':
    #     queryset = User.objects.filter(email__icontains=form['email'].value())
    #     # form.fields['customer'].queryset = User.objects.filter()
    #     context = {
    #         "form": form,
    #         "header": header,
    #         "queryset": queryset,
    #     }
    return render(request, "users/list_customers.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def choose_categories(request):
    header = 'Select a product category'
    queryset = Category.objects.all()
    # pc = Product.objects.filter(category__id='1')
    # pc_count = pc.count()
    context = {
        "header": header,
        "queryset": queryset,
        # "pc_count": pc_count
    }
    return render(request, "choose_categories.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def product_list_customer(request, pk):
    category = Category.objects.get(id=pk)
    queryset = Product.objects.filter(category__id=pk)

    filter = ProductCustomerFilter(request.GET, queryset=queryset)

    #product_paginator = Paginator(queryset, 2)
    title = "Advanced Search"
    product_paginator = Paginator(filter.qs, 2)
    page = request.GET.get('page')
    prods = product_paginator.get_page(page)

    # filter = ProductFilter(request.GET, queryset=prods)
    # prods = filter.qs
    # customer = request.user.customer
    # order, created = Order.objects.get_or_create(customer=customer, status='Pending')
    # items = order.orderitem_set.all()
    # cartItems = order.get_cart_items

    context = {
        'queryset': queryset,
        'prods': prods,
        'shipping': False,
        'filter': filter,
        'title': title,
        # 'cartItems':cartItems
    }
    return render(request, "users/product_list_customer.html", context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'customer'])
# def update_cart(request, pk):
#     if request.method == 'POST':
#         product = request.POST.get('product')
#         remove = request.POST.get('remove')
#         cart = request.session.get('cart')
#         if cart:
#             quantity = cart.get(product)
#             if quantity:
#                 if remove:
#                     if quantity <= 1:
#                         cart.pop(product)
#                     else:
#                         cart[product] = quantity - 1
#                 else:
#                     cart[product] = quantity + 1
#             else:
#                 cart[product] = 1
#         else:
#             cart = {}
#             cart[product] = 1
#
#         request.session['cart'] = cart
#         print(request.session['cart'])
#         return redirect(reverse())
#
#     else:
#         products = Product.objects.all()
#         context = {'products': products}
#         return render(request, 'users/product_list_customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def homePage_customers(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('homePage_customers')

    else:
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'home_customer.html', context)
