from django.shortcuts import render, redirect
from .models import Company
from .forms import *
from invmanagement.models import User, Employee
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from invmanagement.authentications import unauthenticated_user, allowed_users
from django.core.paginator import Paginator
# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def company(request):
    header = 'Companies details'
    #form = CompanySearchForm(request.POST or None)
    # group = request.user.groups.all().name == "customer"
    queryset = Company.objects.all()
    comp_paginator = Paginator(queryset, 2)
    page = request.GET.get('page')
    companies = comp_paginator.get_page(page)
    context = {
        #"form": form,
        "header": header,
        "queryset": queryset,
        "companies": companies,
    }
    # if request.method == 'POST':
    #     queryset = Company.objects.filter(name=form['name'].value())
    #     # form.fields['customer'].queryset = User.objects.filter()
    #     context = {
    #         "form": form,
    #         "header": header,
    #         "queryset": queryset,
    #     }
    return render(request, "companies/list_companies.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def update_company(request, pk):
    title = "Update Company"
    queryset = Company.objects.get(id=pk)
    form = CompanyUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('/companies')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'companies/update_company.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager'])
def deactivate(request, pk):
    queryset = Company.objects.get(id=pk)
    #userid = request.user.id
    usr = User.objects.all().select_related('employee')
    emp = Employee.objects.values_list('user').filter(company__name__contains=queryset,
                                   user__in=usr)
    emp_query = User.objects.filter(pk__in=emp)
    print(emp_query)
    #user = User.objects.get(id=userid)
    if request.method == 'POST':
        #emp_query.is_active=False
        for obj in emp_query:
            obj.is_active=False
            obj.save()
        if queryset.is_active:
            queryset.is_active=False
            queryset.save()
        #emp_query.delete()
        #queryset.delete()

        messages.success(request, 'Company and its employees deactivated successfully!')
        return redirect('/companies')
    return render(request, 'companies/delete_company.html')