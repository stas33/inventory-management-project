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
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings

from invmanagement.views import (
    registerPage,
    registerCustomerPage,
    loginPage,
    logoutUser,
    inactive_employees,
    inactive_managers,
    activate_user,
    home,
    employees,
    create_employee,
    update_employee,
    customers,
    #homePage_customers,
    choose_categories,
    product_list_customer,
    # CustomerAutocomplete
    #update_cart
)
from companies.views import (
    company,
    update_company,
    deactivate
)
from orders.views import (
    orders,
    order_items,
    create_order,
    update_order,
    #cart,
    #submit,
    orderpage,
    mycart,
    checkout,
    updateItem,
    processOrder,
    redirect,
    shipping_info

)
from products.views import (
    categories,
    product_list,
    #products,
    create_product,
    update_product,
    delete_product,
    # ProductAutocomplete
)

urlpatterns = [
    path('register/', registerPage, name="register"),
    path('register-customer/', registerCustomerPage, name="register-customer"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    #url(r'^product-autocomplete/$', ProductAutocomplete.as_view(), name='product-autocomplete'),
    # url(r'^customer-autocomplete/$', CustomerAutocomplete.as_view(), name='customer-autocomplete'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('inactive_employees/', inactive_employees, name='inactive_employees'),
    path('inactive_managers/', inactive_managers, name='inactive_managers'),
    path('activate_user/<str:pk>/', activate_user, name='activate_user'),
    path('orders_list/', orders, name='orders'),
    path('orders_list/<str:pk>/order_items/', order_items, name='order_items'),
    path('orders_list/<str:pk>/shipping/', shipping_info, name='shipping_info'),
    path('orders_list/update_order/<str:pk>/', update_order, name='update_order'),
    path('employee/customers', customers, name='customers'),

    path('products/categories/', categories, name='categories'),
    path('products/categories/<str:pk>/', product_list, name='product_list'),
    #path('products/', products, name='products'),
    path('create_product/', create_product, name='create_product'),
    path('update_product/<str:pk>/', update_product, name="update_product"),
    path('delete_product/<str:pk>/', delete_product, name="delete_product"),
    path('employees/', employees, name="employees"),
    path('create_employee/', create_employee, name='create_employee'),
    path('update_employee/<str:pk>/', update_employee, name="update_employee"),
    path('companies/', company, name="company"),
    path('update_company/<str:pk>/', update_company, name="update_company"),
    path('deactivate/<str:pk>/', deactivate, name="deactivate"),

    # path('home_customer/', homePage_customers, name="homePage_customers"),
    path('customer/products/choose_category/', choose_categories, name="choose_categories"),

    path('customer/products/choose_category/<str:pk>/', product_list_customer, name="product_list_customer"),
    path('customer/mycart/', mycart, name="mycart"),
    path('customer/checkout/', checkout, name="checkout"),
    path('customer/update_item/', updateItem, name="updateItem"),
    path('customer/process_order/', processOrder, name="processOrder"),
    #path('cart/', cart, name="cart"),
    #path('submit/', submit, name="submit"),
    path('customer/myorders/', orderpage, name='orderpage'),
    #path('update_cart/', update_cart, name="update_cart"),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)