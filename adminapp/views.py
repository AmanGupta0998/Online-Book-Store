from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .models import *
from userapp.models import *
from django.views.decorators.cache import cache_control


from decimal import Decimal,InvalidOperation

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context ={
        'adminid':adminid,
        'user_count':UserInfo.objects.all().count(),
        'book_count':Order.objects.all().count(),
        'category_count':Category.objects.all().count(),
        'order_count':Order.objects.all().count(),
        'total_revenue':0,
        'enquiry_count':Enquiry.objects.all().count(),
        
    }
    return render(request,'admindash.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,'You are logged out')
        return redirect('adminlogin')
    else:
        return redirect('index')
    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
   
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    enqs=Enquiry.objects.all() #for enquiry data shows on admin dash
    adminid=request.session.get('adminid')
    return render(request,'viewenq.html',{'enqs':enqs,'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    enq=Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,"Enquiry has been deleted successfully")
    return redirect('viewenq')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def adminchangepwd(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    if request.method=="POST":
        oldpwd=request.POST.get('oldpwd')
        newpwd=request.POST.get('newpwd')
        confirmpwd=request.POST.get('confirmpwd')
        #change password
        try:
            admin=LoginInfo.objects.get(username=adminid)
            if admin.password != oldpwd:
                messages.error(request,"Old Password is Incorrect")
                return redirect('adminchangepwd')
            elif newpwd != confirmpwd:
                messages.error(request,"New Password and Confirm Password both are not same")
                return redirect('adminchangepwd')
            elif admin.password == confirmpwd:
                messages.error(request,"New Password is same as old Password")
                return redirect('adminchangepwd')
            else:
                admin.password=newpwd
                admin.save()
                messages.success(request,"Your Password has been changed successfully")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Siomething went wrong")
            return redirect('adminlogin')
                
    return render(request,'changepass.html',{'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def addcat(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not loggedin")
        return redirect('adminlogin')
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        cat=Category(name=name,description=description)
        cat.save()
        messages.success(request,"Category Added Successfully")
        return redirect('addcat')
    adminid=request.session.get('adminid')
    return render(request,'addcat.html',{'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def viewcat(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not loggedin")
        return redirect('adminlogin')
    category=Category.objects.all()
    adminid=request.session.get('adminid')
    return render(request,'viewcat.html',{'category':category,'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def delcat(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    cat=Category.objects.get(id=id)
    cat.delete()
    messages.success(request,"Category has been deleted successfully")
    return redirect('viewcat')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def addbook(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not loggedin")
        return redirect('adminlogin')
    cats=Category.objects.all()
    if request.method=='POST':
        title=request.POST.get('title')
        author=request.POST.get('author')
        catid=request.POST.get('category')
        cat=Category.objects.get(id=catid)  
        description=request.POST.get('description')
        original_price= Decimal(request.POST.get('original_price'))
        price= Decimal(request.POST.get('price'))
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        book=Book(title=title,author=author,category=cat,description=description,original_price=original_price,price=price,published_date=published_date,language=language,cover_image=cover_image,stock=stock)
        book.save()
        messages.success(request,"New Book is added successfully")
        return redirect('addbook')
    adminid=request.session.get('adminid')
    return render(request,'addbook.html',{'cats':cats,'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def viewbook(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not loggedin")
        return redirect('adminlogin')
    book=Book.objects.all()
    adminid=request.session.get('adminid')
    return render(request,'viewbook.html',{'book':book,'adminid':adminid})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def delbook(request,id):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    book=Book.objects.get(id=id)
    book.delete()
    messages.success(request,"Book has been deleted successfully")
    return redirect('viewbook')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def adminorders(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context ={
        'adminid':adminid,
        'orders':Order.objects.all().order_by('-ordered_at')
    }
    return render(request,'adminorders.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)

def editbook(request,id):
    if 'adminid' not in request.session:
        messages.error(request,"Your are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    book = Book.objects.get(id=id)
    cats = Category.objects.all()
    context = {
        'adminid': adminid,
        'book':book,
        'cats':cats,
    }
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        cat = Category.objects.get(id=category)  # must add
        description = request.POST.get('description')
        original_price = request.POST.get('original_price')
        price = request.POST.get('price')
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        cover_image = request.FILES.get('cover_image')
        stock = request.POST.get('stock')
        book.title = title
        book.author = author
        book.category = cat
        book.description = description
        book.original_price = original_price
        book.price = price
        if published_date:
            book.published_date = published_date
        book.language = language
        if cover_image:
            book.cover_image = cover_image
        book.stock = stock
        book.save()
        messages.success(request, f"{title} is updated successfully")
        return redirect('viewbook')
    return render(request, 'editbook.html',context)


