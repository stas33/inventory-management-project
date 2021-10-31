from django.shortcuts import render, redirect
from .models import Order
from products.models import Product
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
@allowed_users(allowed_roles=['admin', 'employee'])
def orders(request):
    header = 'Submitted orders'
    form = OrderSearchForm(request.POST or None)
    queryset = Order.objects.filter(user__groups__name='customer',
                                    )
    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
    }
    if request.method == 'POST':
        # queryset = Order.objects.filter(user__in=form['user'].value(),
        #                               user__groups__name='customer')
        queryset = Order.objects.filter(status__contains=form['status'].value(),
                                        user__groups__name='customer')
        # form.fields['customer'].queryset = User.objects.filter()
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "orders/list_orders.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee', 'customer'])
def create_order(request):
    form = CreateOrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Order created successfully!')
        return redirect("/employee")
    context = {
        "form": form,
        "title": "Add order",
    }
    return render(request, "orders/create_order.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def update_order(request, pk):
    title = "Update order status"
    queryset = Order.objects.get(id=pk)
    form = OrderUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully!')
            return redirect('/employee')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'orders/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def cart(request):
    cart_product_id = list(request.session.get('cart').keys())
    cart_product = Product.get_products_by_id(cart_product_id)
    return render(request, 'orders/cart.html', {'cart_product': cart_product})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def submit(request):
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        user = request.user.id
        # customer = request.session.get("customer")
        cart = request.session.get("cart")
        products = Product.get_products_by_id(list(cart.keys()))
        for product in products:
            order = Order(user=User(id=user), product=product, price=product.price, address=address,
                          phone=phone, quantity=cart.get(str(product.id)), status="Pending")
            order.save()

        request.session['cart'] = {}
        messages.success(request, 'Order submitted successfully!')
        return redirect("homePage_customers")
    else:
        return render(request, 'orders/submit_order.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def orderpage(request):
    user = request.user.id
    order = Order.get_order_by_customer(user)
    print(order)
    return render(request, 'orders/customer_orders.html', {'order': order})