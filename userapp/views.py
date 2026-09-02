from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from adminapp.models import *
from .models import *


import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views.decorators.cache import cache_control

from django.core.mail import send_mail


# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userdash(request):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    orders=Order.objects.filter(user=user)
    order_items=[]
    for o in orders:
        order_items.append(OrderItem.objects.filter(order=o))
    context={
        'name':user.name,
        'userid':userid,
        'profile':user.profile,
        'order_items':order_items,
        
    }
    return render(request,'userdash.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request,'You are logged out')
        return redirect('login')
    else:
        return redirect('index')  
    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userchangepwd(request):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    context={
        'name':user.name,
        'userid':userid,
        'profile':user.profile
    }
    if request.method=="POST":
        oldpwd=request.POST.get('oldpwd')
        newpwd=request.POST.get('newpwd')
        confirmpwd=request.POST.get('confirmpwd')
        #change password
        try:
            user=LoginInfo.objects.get(username=userid)
            if user.password != oldpwd:
                messages.error(request,"Old Password is Incorrect")
                return redirect('userchangepwd')
            elif newpwd != confirmpwd:
                messages.error(request,"New Password and Confirm Password both are not same")
                return redirect('userchangepwd')
            elif user.password == confirmpwd:
                messages.error(request,"New Password is same as old Password")
                return redirect('userchangepwd')
            else:
                user.password=newpwd
                user.save()
                messages.success(request,"Your Password has been changed successfully")
                return redirect('userdash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Siomething went wrong")
            return redirect('login')
                
    return render(request,'userchangepass.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewcart(request):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    ucart=Cart.objects.filter(user=user).first()
    if ucart is None:
        cart=Cart(user=user)
        cart.save()
    items=CartItem.objects.filter(cart=Cart.objects.filter(user=user).first())
    total=0
    for i in items:
        total=total+i.get_total_price()
    context={
        'name':user.name,
        'userid':userid,
        'profile':user.profile,
        'items':items,
        'total':total
    }
    return render(request,'viewcart.html',context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)    
def addtocart(request,id):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    ucart=Cart.objects.filter(user=user).first()
    if ucart is None:
        cart=Cart(user=user)
        cart.save()
    
    if request.method=='POST':
        quantity=request.POST.get('quantity')
        if quantity is None:
            quantity=1
        book=Book.objects.get(id=id)
        ci=CartItem(cart=Cart.objects.filter(user=user).first(),book=book,quantity=quantity)
        ci.save()
        messages.success(request,"Book added to cart")
        return redirect('viewcart')
    else:
        return redirect('index')
    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def removeitem(request,id):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    ucart=Cart.objects.filter(user=user).first()
    book=Book.objects.get(id=id)
    CartItem.objects.filter(cart=ucart,book=book).delete()
    messages.success(request,"Book removed from cart")
    return redirect('viewcart')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def checkout(request):
    if 'userid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)

    line_items = []

    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(item.book.price * 100),
                'product_data': {
                    'name': item.book.title,
                },
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'sepa_debit'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/userapp/payment-success/'),
        cancel_url=request.build_absolute_uri('/viewcart/'),
    )

    return redirect(session.url, code=303)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def payment_success(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login')

 
    userid=request.session.get('userid')
    user = UserInfo.objects.get(email=userid)

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No items found in your cart.")
            return redirect('index')

  
        total_amount = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )

       
        cart_items.delete()

        items = OrderItem.objects.filter(order=order)

        # Add total_price attribute to each item
        for item in items:
            item.total_price = item.quantity * item.price

        subject='Order Confirmation :'
        msg=f"Dear Reader, {user.name}\n\nThank you for ordering book from our application.\n\nBest Regards :\n\n VIDYA Prakashan Mandir."
        try:
            send_mail(subject=subject,message=msg,recipient_list=[f"{user.email}"],from_email="VIDYA Prakash mandir",fail_silently=True)
        
            messages.success(request, "Payment successful! Your order has been placed.")
            return render(request,'payment_success.html', {'order': order})
        except:
            messages.warning(request,"Payment Successfull ! Your Order has been placed. But mail can't be send.")
            return redirect(request,'payment_success.html',{'order':order})

    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('index')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userorders(request):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    orders=Order.objects.filter(user=user)
    order_items=[]
    for o in orders:
        order_items.append(OrderItem.objects.filter(order=o))
    context={
        'name':user.name,
        'userid':userid,
        'profile':user.profile,
        'order_items':order_items,
    }
    return render(request,'userorders.html',context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userprofile(request):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    context={
        'name':user.name,
        'userid':userid,
        'profile':user.profile,
        'user':user
    }
    return render(request,'userprofile.html',context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def editprofile(request):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid=request.session.get('userid')
    user=UserInfo.objects.get(email=userid)
    context={
        'name':user.name,
        'userid':userid,
        'profile':user.profile,
        'user':user
    }
    if request.method=='POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        address=request.POST.get('address')
        profile=request.FILES.get('profile')
        user.name=name
        user.contactno=contactno
        user.address=address
        if profile:
            user.profile=profile
        user.save()
        messages.success(request,"Profile updated successfully")
        return redirect('userprofile')
    return render(request,'editprofile.html',context)