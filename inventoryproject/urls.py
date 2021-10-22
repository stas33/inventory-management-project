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
from invmanagement import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),

    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('employee/', views.orders, name='orders'),
    path('employee/customers', views.customers, name='customers'),
    #path('manager/', views.home, name='manager'),
    #path('customer/', views.customer_home, name='customer'),

    path('products/', views.products, name='products'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<str:pk>/', views.update_product, name="update_product"),
    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),

    #path('create_order/', views.create_order, name="create_order"),
    path('home_customer/', views.homePage_customers, name="homePage_customers"),
    path('cart/', views.cart, name="cart"),
    path('submit/', views.submit, name="submit"),
    path('myorders/', views.orderpage, name='orderpage'),
    path('update_order/<str:pk>/', views.update_order, name="update_order"),
]

urlpatterns += staticfiles_urlpatterns()
