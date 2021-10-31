"""inventoryproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from invmanagement.views import (
    registerPage,
    registerCustomerPage,
    loginPage,
    logoutUser,
    inactive_users,
    activate_user,
    home,
    employees,
    create_employee,
    update_employee,
    customers,
    homePage_customers
)
from companies.views import (
    company,
    update_company,
    deactivate
)
from orders.views import (
    orders,
    create_order,
    update_order,
    cart,
    submit,
    orderpage
)
from products.views import (
    products,
    create_product,
    update_product,
    delete_product
)

urlpatterns = [
    path('register/', registerPage, name="register"),
    path('register-customer/', registerCustomerPage, name="register-customer"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),

    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('inactive_users/', inactive_users, name='inactive_users'),
    path('activate_user/<str:pk>/', activate_user, name='activate_user'),
    path('employee/', orders, name='orders'),
    path('employee/customers', customers, name='customers'),

    path('products/', products, name='products'),
    path('create_product/', create_product, name='create_product'),
    path('update_product/<str:pk>/', update_product, name="update_product"),
    path('delete_product/<str:pk>/', delete_product, name="delete_product"),
    path('employees/', employees, name="employees"),
    path('create_employee/', create_employee, name='create_employee'),
    path('update_employee/<str:pk>/', update_employee, name="update_employee"),
    path('companies/', company, name="company"),
    path('update_company/<str:pk>/', update_company, name="update_company"),
    path('deactivate/<str:pk>/', deactivate, name="deactivate"),

    path('home_customer/', homePage_customers, name="homePage_customers"),
    path('cart/', cart, name="cart"),
    path('submit/', submit, name="submit"),
    path('myorders/', orderpage, name='orderpage'),
    path('update_order/<str:pk>/', update_order, name="update_order"),
]

urlpatterns += staticfiles_urlpatterns()
