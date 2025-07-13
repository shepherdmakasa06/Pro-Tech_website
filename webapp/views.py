from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Customer
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
from .models import Receipt, ReceiptItem


# Create your views here.
def index(request):
    return render (request, 'index.html')

def generate_verification_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def send_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
        verification_code = generate_verification_code()
        request.session['verification_code'] = verification_code
        request.session['email_to_verify'] = email
        try:
            send_mail(
                'Email Verification',
                f'Your verification code is: {verification_code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'Verification email sent'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Failed to send verification email: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def verify_email_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = request.session.get('verification_code')
        if code == stored_code:
            request.session['email_verified'] = True
            return JsonResponse({'success': True, 'message': 'Email verified'})
        return JsonResponse({'success': False, 'error': 'Invalid verification code'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if not request.session.get('email_verified'):
            messages.error(request, 'Please verify your email first!')
            return redirect('register')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken!😒')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken!😒')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Clear verification session data
                request.session.pop('email_verified', None)
                request.session.pop('verification_code', None)
                request.session.pop('email_to_verify', None)
                return redirect('login')
        else:
            messages.info(request, 'Password not matching!😒😒')
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
        contact_number = request.POST['contact_number']
        address = request.POST['address']
        
        customer = Customer(name=name, contact_number=contact_number, address=address)
        customer.save()
        
        messages.success(request, 'Customer added successfully!')
        return redirect('view_customers')
    
    return render(request, 'counter.html')

@login_required
def view_customers(request):
    try:
        customers = Customer.objects.all()
        return render(request, 'view_customers.html', {'customers': customers})
    except Exception as e:
        return render(request, 'view_customers.html', {'customers': [], 'error': str(e)})

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if not user.check_password(current_password):
            return JsonResponse({'success': False, 'error': 'Current password is incorrect.'})
        if new_password != confirm_new_password:
            return JsonResponse({'success': False, 'error': 'New passwords do not match.'})
        if len(new_password) < 8:
            return JsonResponse({'success': False, 'error': 'New password must be at least 8 characters.'})
        user.set_password(new_password)
        user.save()
        # Send email notification
        send_mail(
            'Password Changed',
            'Your password has been changed successfully',
            'shepherdmakasa06@gmail.com',
            [user.email],
            fail_silently=True,
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
def save_receipt(request):
    if request.method == 'POST':
        user = request.user
        customer_name = request.POST.get('customer_name')
        invoice_number = request.POST.get('invoice_number')
        total_amount = request.POST.get('total_amount')
        items_json = request.POST.get('items')
        if not (customer_name and invoice_number and total_amount and items_json):
            return JsonResponse({'success': False, 'error': 'Missing required fields.'}, status=400)
        try:
            receipt = Receipt.objects.create(
                user=user,
                customer_name=customer_name,
                invoice_number=invoice_number,
                total_amount=total_amount
            )
            items = json.loads(items_json)
            for item in items:
                ReceiptItem.objects.create(
                    receipt=receipt,
                    description=item['description'],
                    quantity=int(item['quantity']),
                    unit_price=float(item['unit_price']),
                    total=float(item['total'])
                )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})