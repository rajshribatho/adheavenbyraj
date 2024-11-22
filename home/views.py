from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.db.models import Q
from home.models import HomeTable,UserInfo,ListTable,OrderHistory,Payment_history
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
import razorpay
from django.shortcuts import render,redirect
from .models import ListTable  
from django.conf import settings
from .models import OrderHistory
from django.core.mail import send_mail
from .models import HomeTable



# Create your views here.
def register_user(request):
   data ={}
   if request.user.is_authenticated:
      if request.user.is_superuser:
         return redirect("/admin")
      else:
         return redirect("/")
   if request.method=="POST":
      uname=request.POST.get('username')
      passw=request.POST.get('password')
      pass2=request.POST.get('password2')
      
      if (uname=="" or passw=="" or pass2==""):
         data['error_msg']="Fields cant be empty"
      elif(passw!=pass2):
         data['error_msg']="Password Does not matched"
      elif(User.objects.filter(username=uname).exists()):
         data['error_msg']=uname + " already exist"
      else:
         user=User.objects.create(username=uname)
         user.set_password(passw)
         user.save()
         
         mailid=request.POST.get('mailid')
         phoneno=request.POST.get('contactnumber')
         user_info=UserInfo.objects.create(user_id=user,mailid=mailid,phoneno=phoneno)
         user_info.save()
         return redirect("/")
   return render(request,'register.html',context=data)
# userinfo = User_info.objects.create(user_id=user,phone=)


def login_user(request):
   data ={}
   if request.user.is_authenticated:
      if request.user.is_superuser:
         return redirect("/view_advertisements")
      else:
         return redirect("/")
      
      
      
   if request.method=="POST":
      uname=request.POST.get('username')
      upass=request.POST.get('password')
      
      if (uname=="" or upass==""):
         data['error_msg']="Fields cant be empty"
      elif(not User.objects.filter(username=uname).exists()):
         data['error_msg']=uname + " user does not exist"
      else:
         user=authenticate(username=uname,password=upass)
         if user is None:
            data['error_msg']="Wrong password"
         else:
            login(request,user)
            if user.is_superuser:
               return redirect("/view_advertisements")
            else:
               return redirect("/services")
   return render(request,'login.html',context=data)



def user_logout(request):
   logout(request)
   return redirect('/')


def admin_user(request):
   if request.user.is_authenticated:
      if not request.user.is_superuser:
         return redirect("/")
   return render(request,'view_advertisements')


def add_advertising(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        marketingtype = request.POST.get('marketingtype')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        if category and marketingtype and price and image:
            home = HomeTable.objects.create(
                category=category,
                marketingtype=marketingtype,
                price=price,
                image=image
            )
            home.save()
            return redirect("/view_advertisements")
        else:
            error_msg = "All fields are required."
            return render(request, "admin/advertisement/add_advertisement.html", {"error_msg": error_msg})
    
    return render(request, "admin/advertisement/add_advertisement.html")




# views.py

def view_advertisements(request):
    data = {}
    advertisements = HomeTable.objects.all()
    data['advertisements'] = advertisements
    return render(request, 'admin/advertisement/view_advertisements.html', context=data)


def delete_advertisement(request,advertisementid):
   advertisements=HomeTable.objects.get(id=advertisementid)
   advertisements.delete()
   return redirect("/view_advertisements/")



def searchByName(request):
    data = {}
    if (request.method == "POST"):
        product_name = request.POST.get("product_name")
        print("searching for",product_name)
        searched_products = HomeTable.objects.filter(marketingtype__icontains=product_name)
        data['advertisements'] = searched_products
        print("searching product is ",searched_products)
        return render(request, 'services.html', context=data)
    return redirect("/")

def price_range(request):
    print("in search")
    data = {}

    # Get min and max prices from POST request, or default to empty strings
    min_price = request.POST.get('min', '').strip()
    max_price = request.POST.get('max', '').strip()
    
    # Check if both fields are empty
    if not min_price and not max_price:
        data['message'] = "Please enter both minimum and maximum price values."
    else:
        # Convert to int if not empty; use default values if empty
        min_price = int(min_price) if min_price else 0
        max_price = int(max_price) if max_price else 1000000

        # Build queries
        q1 = Q(is_available=True)
        q2 = Q(price__gte=min_price)
        q3 = Q(price__lte=max_price)
        
        # Filter advertisements
        searched_advertisements = filtered_advertisements.filter(q1 & q2 & q3)
        data['advertisements'] = searched_advertisements

    return render(request, 'services.html', context=data)



def edit_advertisements(request,advertisementid):
   data={}
   advertisements=HomeTable.objects.get(id=advertisementid)
   data['advertisements']=advertisements
   if request.method=='POST':
      advertisements.category = request.POST.get('category')
      advertisements.marketingtype = request.POST.get('marketingtype')
      advertisements.price = request.POST.get('price')
      if request.FILES['image'] :
         advertisements.image = request.FILES['image']
      advertisements.save()
     
     
      return redirect('/view_advertisements/')
   return render(request,'admin/advertisement/update_advertisement.html',context=data)


advertisements = HomeTable.objects.filter()

def user_services(request):
   data = {}
   global advertisements
   global filtered_advertisements
   advertisements = HomeTable.objects.filter()
   filtered_advertisements = advertisements
   data['advertisements'] = advertisements
   return render(request,'services.html',context=data)


def add_to_list(request, advertisementid):
    if request.user.is_authenticated:
        user = request.user
        advertisements = HomeTable.objects.get(id=advertisementid)
        q1 = Q(user_id=user.id)
        q2 = Q(fadvertisement_id=advertisementid)
        list_entry = ListTable.objects.filter(q1 & q2)
        if list_entry.count() > 0:
            messages.error(request, "Product is already in the cart")
        else:
            list_entry = ListTable.objects.create(user_id=user, fadvertisement_id=advertisements)
            list_entry.save()
            messages.success(request, "Product is added to the cart")
        return redirect('/services')
    else:
        return redirect('/login')



def show_list(request):
    data = {}
    total_items = 0
    total_price = 0
    user_id = request.user.id
    advertisements_in_list = ListTable.objects.filter(user_id=user_id)
    advertisement_details = []
    for advertisement in advertisements_in_list:
        item_total = advertisement.fadvertisement_id.price * advertisement.quantity
        advertisement_details.append({
            'id': advertisement.id,
            'category': advertisement.fadvertisement_id.category,
            'price': advertisement.fadvertisement_id.price,
            'quantity': advertisement.quantity,
            'marketingtype': advertisement.fadvertisement_id.marketingtype,
            'total': item_total
        })
        total_items += advertisement.quantity
        total_price += item_total
    data['advertisementlist'] = advertisement_details
    data['total_items'] = total_items
    data['total_price'] = total_price
    return render(request, 'cart.html', context=data)

import razorpay

def order(request, payment_id, amount):
    pay = Payment_history.objects.create(id=payment_id, user_id=request.user, amount=amount)
    list_items = ListTable.objects.filter(user_id=request.user.id)
    user_info = UserInfo.objects.get(user_id=request.user.id)
    
    for item in list_items:
        total_price = item.quantity * item.fadvertisement_id.price
        OrderHistory.objects.create(
            user=request.user,
            advertisement=item.fadvertisement_id,
            quantity=item.quantity,
            total_price=total_price
        )
    list_items.delete()
    return redirect("/order_history") 


def order_history(request):
    if request.user.is_authenticated:
        orders = OrderHistory.objects.filter(user=request.user).order_by('-order_date')
        return render(request, 'order_history.html', {'orders': orders})
    else:
        return redirect('/login')

import logging
logger = logging.getLogger(__name__)
def make_payment(request):
    total_price = 0
    advertisements_in_list = ListTable.objects.filter(user_id=request.user.id)
    for advertisement in advertisements_in_list:
        total_price += (advertisement.fadvertisement_id.price * advertisement.quantity)
    client = razorpay.Client(auth=("rzp_test_1l5VCpbFpucFG9", "W8W72M7tTmqcIkFK5C6Baru0"))
    data = {
        "amount": int(total_price * 100),  # Amount in paise
        "currency": "INR",
        "receipt": "order_rcptid_11"
    }
    payment = client.order.create(data=data)
    if request.method == 'POST':
        logger.info("Payment POST request received")
        try:
            for advertisement in advertisements_in_list:
                logger.info(f"Creating OrderHistory for user {request.user.id} and advertisement {advertisement.fadvertisement_id.id}")
                OrderHistory.objects.create(
                    user=request.user,
                    advertisement=advertisement.fadvertisement_id,
                    quantity=advertisement.quantity,
                    total_price=advertisement.fadvertisement_id.price * advertisement.quantity
                )
            advertisements_in_list.delete()
            messages.success(request, "Payment successful and order placed!")
            return redirect('/order_history')
        except Exception as e:
            logger.error(f"Error creating OrderHistory: {e}")
            messages.error(request, "An error occurred while processing your order. Please try again.")

    context = {
        'amount': data['amount'],
        'order_id': payment['id'],
        'api_key': "rzp_test_1l5VCpbFpucFG9"
    }
    return render(request, 'payment.html', context)




def filter_by_category(request,category_value):
   data={}
   q1 = Q(is_available=True)
   q2 = Q(category=category_value)
   global advertisements
   global filtered_advertisements
   filtered_advertisements=advertisements.filter(q1 & q2)
   data['advertisements']=filtered_advertisements
   return render(request,'services.html',context=data)



def delete_list(request,fadvertisementid):
    list_item = ListTable.objects.get(id=fadvertisementid)
    list_item.delete()
    return redirect("/show_list")

def find_list_value(request):
   user=request.user.id
   list=ListTable.objects.filter(uid=user)
   list_count=list.count()
   return list_count






def admin_order_history(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = OrderHistory.objects.all().order_by('-order_date')
        orders_with_phone = []
        for order in orders:
            user_info = UserInfo.objects.get(user_id=order.user.id)
            order_with_phone = {
                'order': order,
                'phone': user_info.phoneno
            }
            orders_with_phone.append(order_with_phone)
        return render(request, 'admin/admin_order.html', {'orders_with_phone': orders_with_phone})
    else:
        return redirect('/login')

import random
def forgot_password(request):
    if request.method == "POST" :
        uname = request.POST['username']
        if User.objects.filter(username=uname).exists() :
            user = User.objects.get(username=uname)
            userinfo=UserInfo.objects.get(user_id=user.id)
            url = "/forgotpassword/update/" + user.username
            global otp
            otp = random.randint(1111,9999)
            send_mail(
    "otp for password change - Pawsitive care" ,
    "Your otp is " + str(otp),
    settings.EMAIL_HOST_USER,
    [userinfo.mailid],
    fail_silently=False,)
            return redirect(url)
    return render(request,"forgotpassword.html")


def passotp(request,uname):
    user = User.objects.get(username=uname)
    data = {}
    if request.method == "POST":
        uotp = request.POST['otp']
        uotp = int(uotp)
        password = request.POST['password']
        confpass = request.POST['confpass']
        global otp
        if uotp != otp :
            print(uotp,type(uotp),otp,type(otp))
            data['error'] = "otp does not match"
        elif password != confpass :
            data['error'] = "passwords do not match"
        elif uotp == otp and password == confpass : 
            user.set_password(password)
            user.save()
            otp = None 
            return redirect("/login")
    return render(request,"otppass.html",context=data)

def home(request):
    return render(request,'home.html')
def admin(request):
    return render(request,'admin.html')
def about(request):
    return render(request,'about.html')