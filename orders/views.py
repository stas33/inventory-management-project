from django.shortcuts import render, redirect
from .models import *
from products.models import Product
from .forms import *
from .filters import *
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from invmanagement.authentications import unauthenticated_user, allowed_users
import datetime
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from dal import autocomplete
import smtplib


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def orders(request):
    header = 'Submitted orders'

    queryset = Order.objects.all().order_by('id')
    filter = OrderSearchFilter(request.GET, queryset=queryset)
    title = "Advanced Search"
    order_paginator = Paginator(filter.qs, 2)
    page = request.GET.get('page')
    ord = order_paginator.get_page(page)

    context = {
        "header": header,
        "queryset": queryset,
        "filter": filter,
        "title": title,
        "ord": ord,
    }

    return render(request, "orders/list_orders.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee', 'customer'])
def order_items(request, pk):
    header = f'Items of order with id { {pk} }'
    queryset = OrderItem.objects.filter(order__id=pk)

    context = {
        "header": header,
        "queryset": queryset,
    }

    return render(request, "orders/order_items.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee', 'customer'])
def shipping_info(request, pk):
    header = f'Shipping info for order with id { {pk} }'
    queryset = Shipping.objects.filter(order__id=pk)
    context = {
        "header": header,
        "queryset": queryset
    }
    return  render(request, "orders/shipping_info.html", context)


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
            if form.cleaned_data.get("status") == 'Approved':
                ord_items = OrderItem.objects.filter(order__id=pk)
                for item in ord_items:
                    prod = Product.objects.get(id=item.product.id)
                    if prod.quantity > 0:
                        prod.quantity = (prod.quantity - item.quantity)
                        prod.save()

            mail = queryset.customer.email
            status = form.cleaned_data.get("status")
            order_id = queryset.transaction_id
            customer_name = queryset.customer.name
            send_mail(status, order_id, mail, customer_name)
            queryset.status = form.cleaned_data.get("status")
            queryset.save()
            form.save()
            messages.success(request, f'Order status updated successfully! Email sent to customer {queryset.customer.name}')
            return redirect('/orders_list')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'orders/create_order.html', context)


def send_mail(status, order_id, mail, customer_name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('sendmailnotification8@gmail.com', 'anjdwsfdpqxngngt')
    subject = f"Status update for order {order_id} of customer {customer_name}"
    body = f"The status for your order has been changed. Current status: {status}"
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'sendmailnotification8@gmail.com',
        f'{mail}',
        msg
    )
    print("Email has been sent!")
    server.quit()


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def mycart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='Pending')
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cart = {}
        print('CART:', cart)
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/my_cart.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='Pending')

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, status='Pending')
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    #data_ordered = datetime.datetime.now()
    data = json.loads(request.body)

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, status='Pending')
    #order, created = Order.objects.create(customer=customer, status='Pending', date_ordered=date_ordered,
    #                                      transaction_id=transaction_id)
    # total = data['form']['total']
    order.transaction_id = transaction_id
    order.save()

    if order.shipping == True:
        Shipping.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            phone=data['shipping']['phone'],
        )
    send_order_confirmation(order.status, order.transaction_id, order.customer.email, order.customer.name)
    items = []

    return JsonResponse('Completed!', safe=False)


def send_order_confirmation(status, order_id, mail, customer_name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('sendmailnotification8@gmail.com', 'anjdwsfdpqxngngt')
    subject = f"Order confirmation of customer {customer_name}"
    body = f"You have successfully created/modified an order with id {order_id}!"
    body2 = f"Once order status is changed, you will receive another email."
    body3 = f"Current order status: {status}"
    msg = f"Subject: {subject}\n\n{body}\n{body2}\n{body3}"
    server.sendmail(
        'sendmailnotification8@gmail.com',
        f'{mail}',
        msg
    )
    print("Email has been sent!")
    server.quit()


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def orderpage(request):
    customer = request.user.customer
    title = f"Orders of Customer { customer.name }"
    orders = Order.objects.filter(customer=customer)
    return render(request, 'orders/myorders.html', {'orders': orders, 'title': title})
