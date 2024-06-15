from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import User,auth
from django.contrib import messages
import datetime
# Create your views here.
def index(request):
    #to display cart total in nav bar
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,complete=False)  #if the order exists and is not complete get the order else create a new order
        items=order.orderitem_set.all()
        cartItems=order.get_cart_quantity
    else:
        items=[]
        order={'get_cart_quantity':0,'get_cart_total':0}
        cartItems = order['get_cart_quantity']

    products=product.objects.all()
    return render(request,'index.html',{'products':products,'cartItems':cartItems})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,complete=False)  #if the order exists and is not complete get the order else create a new order
        items=order.orderitem_set.all()
        cartItems=order.get_cart_quantity     #to display cart total in nav bar
    else:
        items=[]
        order={'get_cart_quantity':0,'get_cart_total':0}
        cartItems=order['get_cart_quantity']

    return render(request,'cart.html',{'items':items,'order':order,'cartItems':cartItems})

def search(request):
    return render(request,'search.html')

def productview(request,myid):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,complete=False)  #if the order exists and is not complete get the order else create a new order
        items=order.orderitem_set.all()
        cartItems=order.get_cart_quantity     #to display cart total in nav bar
    else:
        items=[]
        order={'get_cart_quantity':0,'get_cart_total':0}
        cartItems=order['get_cart_quantity']

    prod=product.objects.filter(product_id=myid)
    return render(request,'productview.html',{'product':prod[0],'cartItems':cartItems})

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,complete=False)  #if the order exists and is not complete get the order else create a new order
        items=order.orderitem_set.all()
        cartItems=order.get_cart_quantity     #to display cart total in nav bar
    else:
        items=[]
        order={'get_cart_quantity':0,'get_cart_total':0}
        cartItems=order['get_cart_quantity']
    return render(request,'checkout.html',{'items':items,'order':order,'cartItems':cartItems})

def updateItem(request):
    data= json.loads(request.body)  #to parse the string data
    productId= data['productId']
    action= data['action']
    print(productId)
    print(action)

    customer= request.user.customer
    prod= product.objects.get(product_id=productId)
    order,created= Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=prod)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added ',safe=False)

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        name=request.POST['name']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:      #checks if repeat password is equal to original password
            if User.objects.filter(email=email).exists():   #checks if the email entered already exists in database
                messages.info(request,'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():   #checks if the username entered already exists in database
                messages.info(request,'username already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)  #creates a user if all conditions are satisfied
                user.save();
                customer = Customer.objects.create(user=user, name=name, email=email)
                customer.save();
                return redirect('login')
        else:
            messages.info(request,'password is not same')
            return redirect('register')
    else:        
        return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)   #checks if the user already registered in database

        if user is not None:    #if user exists
            auth.login(request,user)
            return redirect('/shop/')
        else:
            messages.info(request,'credentials invalid')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/shop/')

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
          
        order.transaction_id = transaction_id

        #if total == order.get_cart_total:   #to avoid manipulation of total amount by user
        order.complete = True
        order.save();

        shippingaddress=ShippingAddress.objects.create(
            customer=customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
        shippingaddress.save();
    else:
        print("User not logged in..")
    return JsonResponse('Payment complete',safe=False)