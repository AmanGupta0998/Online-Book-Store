from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from adminapp.models import Book
import requests

# Create your views here.
def index(request):
    context={   
        'userid': request.session.get('userid'),
        'books' : Book.objects.all(),
        'new_arrivals':Book.objects.all()[:3],
        'comic':Book.objects.filter(category__name='Comics')
    }
    return render(request,'index.html',context)

def category(request):
    context={
        'userid': request.session.get('userid'),
        'comic':Book.objects.filter(category__name='Comics'),
        'autography':Book.objects.filter(category__name='Autography'),
        'psy':Book.objects.filter(category__name='psychology')
        
    }
    return render(request,'category.html',context)

def about(request):
    context={
        'userid': request.session.get('userid'),
       
    }
    return render(request,'about.html',context)
def contact(request):
    context={
        'userid': request.session.get('userid'),
       
    }
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        message=request.POST.get('message')
        enq=Enquiry(name=name,email=email,contactno=contactno,message=message)
        enq.save()
       

        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contactno}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }

        response = requests.get(url, params=params)
        print("Response:", response.text)

        messages.success(request,"Your enquiry has been submitted successfully.")
        return redirect('contact')
    
    return render(request,'contact.html',context)

def register(request):
    context={
        'userid': request.session.get('userid'),
       
    }
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password != cpassword:
            messages.error(request,"Password and Confirm Password should be same")
            return redirect('register')
        ch=LoginInfo.objects.filter(username=email)
        if ch:
            messages.error(request,"Email already exists.")
            return redirect('register')
        log=LoginInfo(usertype="user",username=email,password=password)
        user=UserInfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,"Registration is done successfully.")
        return redirect('register')
    return render(request,'register.html',context)

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=LoginInfo.objects.get(usertype="user",username=username,password=password)
            if user is not None:
                request.session['userid']=username
                messages.success(request,"Welcome User")
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request,'login.html')

def shopnow(request):
    return render(request,'shopnow.html')

def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            ad=LoginInfo.objects.get(username=username,password=password)
            if ad is not None:
                request.session['adminid']=username  #security purpose
                messages.success(request,"Welcome Admin")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid Username or Password")
            return redirect('adminlogin')
        
    return render(request,'adminlogin.html')

def aboutdev(request):
    return render(request,'aboutdev.html')


def book_details(request,id):
    context={
        'userid': request.session.get('userid'),
        'book':Book.objects.get(id=id)
    }
    return render(request,'book_details.html',context)

