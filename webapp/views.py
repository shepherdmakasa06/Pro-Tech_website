from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Customer


# Create your views here.
def index(request):
    return render (request, 'index.html')

def register(request):
    if request.method =='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken!😒')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken!😒')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                print('User created😁')
                return redirect('login')
        else:
            messages.info(request,'Password not matching!😒😒')
            return redirect('register')
    else:
        return render(request, 'register.html') 

def login(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('counter')
        else:
            messages.info(request,'Credentials Invalid!😒')
            return redirect('login')
    else:    
         return render (request,'login.html')

def counter(request):
   
    return render (request, 'counter.html' )

def add_customer(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        
        customer = Customer(name=name, email=email, phone=phone, address=address)
        customer.save()
        
        messages.success(request, 'Customer added successfully!')
        return redirect('view_customers')
    
    return render(request, 'add_customer.html')

def view_customers(request):
    customers = Customer.objects.all()
    return render(request, 'view_customers.html', {'customers': customers})