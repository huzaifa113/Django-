from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from math import ceil
import json


# Create your views here.


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('Email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already Taken')
            return render(request, 'shop/register.html')


        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email
        )
        
        user.set_password(password)
        user.save()
        return redirect('/shop/login')
    
    return render(request, 'shop/register.html')
    

        
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            messages.error(request, 'Username is required')
            return render(request, 'shop/login.html')

        if not password:
            messages.error(request, 'Password is required')
            return render(request, 'shop/login.html')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return render(request, 'shop/login.html')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return render(request, 'shop/login.html')
        
        else:
            auth_login(request, user)
            return redirect('/shop/checkout')

    return render(request, 'shop/login.html')



def logout_view(request):
    logout(request)
    return redirect('/shop/checkout')



def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)



def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 :
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)



def about(request):
    return render(request, 'shop/about.html')



def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})



def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productView(request, myid):
    product = Product.objects.get(id=myid)
    query = product.category
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        if cat == query:
            prodtemp = Product.objects.filter(category=cat).exclude(id=myid)  # Exclude the current product
            prod = list(prodtemp)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            if len(prod) != 0:
                allProds.append([prod, range(1, nSlides), nSlides])
    
    return render(request, 'shop/prodView.html', {'product': product, 'allProds': allProds})



@login_required
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html',{'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')