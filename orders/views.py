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


# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def orders(request):
    header = 'Submitted orders'
    # form = OrderSearchForm(request.POST or None)
    # queryset = Order.objects.filter(user__groups__name='customer',
    #                                 )
    queryset = Order.objects.all()
    filter = OrderSearchFilter(request.GET, queryset=queryset)
    queryset = filter.qs
    title = "Advanced Search"

    context = {
        # "form": form,
        "header": header,
        "queryset": queryset,
        "filter": filter,
        "title": title,
    }
    # if request.method == 'POST':
    #     # queryset = Order.objects.filter(user__in=form['user'].value(),
    #     #                               user__groups__name='customer')
    #     queryset = Order.objects.filter(status__contains=form['status'].value(),
    #                                     user__groups__name='customer')
    #     # form.fields['customer'].queryset = User.objects.filter()
    #     context = {
    #         "form": form,
    #         "header": header,
    #         "queryset": queryset,
    #     }
    return render(request, "orders/list_orders.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'employee'])
def order_items(request, pk):
    header = f'Items of order with id { {pk} }'
    # form = OrderSearchForm(request.POST or None)
    # queryset = Order.objects.filter(user__groups__name='customer',
    #                                 )
    queryset = OrderItem.objects.filter(order__id=pk)

    context = {
        # "form": form,
        "header": header,
        "queryset": queryset,
    }

    return render(request, "orders/order_items.html", context)


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
            return redirect('/orders_list')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'orders/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def mycart(request):
    # cart_product_id = list(request.session.get('cart').keys())
    # customer = request.user.customer
    # order, created = Order.objects.get_or_create(customer=customer, status='Pending')
    # #items = Product.get_products_by_id(cart_product_id)
    # items = OrderItem.orderitems_by_product_id(cart_product_id)
    # return render(request, 'orders/my_cart.html', {'items': items, 'order': order})
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
    # cart_product_id = list(request.session.get('cart').keys())
    # cart_product = Product.get_products_by_id(cart_product_id)
    # return render(request, 'orders/my_cart.html', {'cart_product': cart_product, 'order': order})


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'customer'])
# def cart(request):
#     cart_product_id = list(request.session.get('cart').keys())
#     cart_product = Product.get_products_by_id(cart_product_id)
#     return render(request, 'orders/cart.html', {'cart_product': cart_product})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='Pending')
    # order, created = Order.objects.filter(customer=customer, status='Pending')
    # if not orders.exists():
    #     order, created = Order.objects.create(customer=customer, status='Pending')
    # else:
    #     order, created = orders.last()
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
        #Order.objects.

    items = []
    #cartItems = order.get_cart_items

    return JsonResponse('Completed!', safe=False)
    #return redirect("/customer/myorders/")


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'customer'])
# def submit(request):
#     if request.method == "POST":
#         address = request.POST.get("address")
#         phone = request.POST.get("phone")
#         user = request.user.id
#         # customer = request.session.get("customer")
#         cart = request.session.get("cart")
#         products = Product.get_products_by_id(list(cart.keys()))
#         for product in products:
#             order = Order(user=User(id=user), product=product, price=product.price, address=address,
#                           phone=phone, quantity=cart.get(str(product.id)), status="Pending")
#             order.save()
#
#         request.session['cart'] = {}
#         messages.success(request, 'Order submitted successfully!')
#         return redirect("homePage_customers")
#     else:
#         return render(request, 'orders/submit_order.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def orderpage(request):
    # user = request.user.id
    # order = Order.get_order_by_customer(user)
    # print(order)
    customer = request.user.customer
    title = f"Orders of Customer { customer.name }"
    # customer_id
    orders = Order.objects.filter(customer=customer)
    # orderItems = OrderItem.objects.filter(order__customer=customer)
    return render(request, 'orders/myorders.html', {'orders': orders, 'title': title})
