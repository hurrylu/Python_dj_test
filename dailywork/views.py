# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import RequestContext
from dailywork.models import Products, Process, Produce, Material, Worker
from dailywork.forms import ProductForm, ProcessForm, MaterialForm, ProduceForm, WorkerForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def encode_url(str):
    return str.replace('', '_')

def decode_url(str):
    return str.replace('_', '')

# Create your views here.
def index(request):
    request.session.set_test_cookie()
#    context = RequestContext(Request)
    product_list = Products.objects.order_by('product_id')
    context_dict = {'products': product_list}

    for product in product_list:
        product.url = encode_url(product.product_name)

    return render(request, 'dailywork/index.html', context_dict)
#    return HttpResponse("<h1>Welcome to this site!"
#                        "<p><a href='/dailywork/about'>about</a></p></h1>")

def product_table(request):
    request.session.set_test_cookie()
    product_list = Products.objects.order_by('product_id')
    context_dict = {'products': product_list}
    for product in product_list:
        product.url = encode_url(product.product_name)
    return render(request, 'dailywork/product_table.html', context_dict)

def page_product(request, product_id):
#    product_name = decode_url(product_name_url)
    context_dict = {'product_id': product_id}
    try:
        product = Products.objects.get(product_id__iexact=product_id)
        produce_list = Produce.objects.filter(product=product)
        context_dict['produce_list'] = produce_list
        context_dict['product'] = product
    except  Products.DoesNotExist:
        pass

    return render(request, "dailywork/product.html", context_dict)

def process_table(request):
    process_list = Process.objects.order_by('id')
    context_dict = {'process_list': process_list}
    return render(request, 'dailywork/process_table.html', context_dict)

def material_table(request):
    material_list = Material.objects.order_by('id')
    context_dict = {'material_list': material_list}
    return render(request, 'dailywork/material_table.html', context_dict)

def worker_table(request):
    worker_list = Worker.objects.order_by('worker_id')
    context_dict = {'worker_list': worker_list}
    return render(request, 'dailywork/worker_table.html', context_dict)

def about(request):
    context_dic = {}
    return render(request, "dailywork/about.html", context_dic)

def add_product(request):
    if request.method == 'POST':
        formset = ProductForm(request.POST)
        if formset.is_valid():
            formset.save()
            return index(request)
        else:
            print formset.errors
    else:
        formset = ProductForm()
    return render(request, "dailywork/add_product.html", {'formset': formset})

def add_process(request):
    if request.method == 'POST':
        formset = ProcessForm(request.POST)
        if formset.is_valid():
            formset.save()
            return material_table(request)
        else:
            print formset.errors
    else:
        formset = ProcessForm()
    return render(request, "dailywork/add_process.html", {'formset': formset})

def add_material(request):
    print request.method
    if request.method == 'POST':
        print request.method
        formset = MaterialForm(request.POST)
        print formset
        if formset.is_valid():
            formset.save()
            return material_table(request)
        else:
            print formset.errors
    else:
        formset = MaterialForm()
        print "MARK"
        print request.method
    return render(request, "dailywork/add_material.html", {'formset': formset})

def add_produce(request, product_id):
#    product_name = decode_url(product_name_url)
#    context_dict = {'product_name_url': product_name_url, 'product_name': product_name}
    context_dict = {'product_id': product_id}
    if request.method == 'POST':
        formset = ProduceForm(request.POST)
        if formset.is_valid():
            produce = formset.save(commit=False)
            try:
                product = Products.objects.get(product_id__iexact=product_id)
                produce.product = product
            except Products.DoesNotExist:
                return render(request, "dailywork/product.html", {})
            produce.save()
            return page_product(request, product_id)
        else:
            print formset.errors
    else:
        formset = ProduceForm()
    context_dict['formset'] = formset
    return render(request, "dailywork/add_produce.html", context_dict)

class ProductAdd(CreateView):
    model = Products
    fields = '__all__'

class ProductUpdate(UpdateView):
    model = Products
    fields = ['product_id', 'product_name', 'order_num', 'deliver_date']

class ProductDelete(DeleteView):
    model = Products
    success_url = reverse_lazy('product_table')

class ProcessAdd(CreateView):
    model = Process
    fields = '__all__'

class ProcessUpdate(UpdateView):
    model = Process
    fields = ['name', 'code']

class ProcessDelete(DeleteView):
    model = Process
    success_url = reverse_lazy('process_table')

class MaterialAdd(CreateView):
    model = Material
    fields = '__all__'

class MaterialUpdate(UpdateView):
    model = Material
    fields = ['name', 'code', 'inventory', 'used']

class MaterialDelete(DeleteView):
    model = Material
    success_url = reverse_lazy('material_table')

class WorkerAdd(CreateView):
    model = Worker
    fields = '__all__'

class WorkerUpdate(UpdateView):
    model = Worker
    fields = ['worker_id', 'worker_name', 'is_operator', 'is_inspector', 'description']

class WorkerDelete(DeleteView):
    model = Worker
    success_url = reverse_lazy('worker_table')

class ProduceAdd(CreateView):
    model = Produce
    form_class = ProduceForm

class ProduceUpdate(UpdateView):
    model = Produce
    form_class = ProduceForm
#    fields = ['process', 'material', 'assigned_num', 'operator', 'produce_num', 'process_des', 'detect_log', 'inspect_log', 'inspect_date', 'inspector', 'description']

class ProduceDelete(DeleteView):
    model = Produce
    def get_success_url(self):
        return self.object.get_absolute_url()

def report_worker(request):
    return render(request, "dailywork/report_worker.html", {})

def register(request):
    registered = False
    print request.method
    if request.method == 'POST':
        print request.POST
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        print user_form
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, "dailywork/register.html", context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dailywork/')
            else:
                return HttpResponse('您的账号已被禁用！')
        else:
            print "登录信息有误：{0}, {1}" .format(username, password)
            return HttpResponse("无效的登录账户或密码！")
    else:
        return render(request, "dailywork/login.html", {})

@login_required
def restricted(request):
    return HttpResponse("账号受限，仅能登录此页面！")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/dailywork/')
