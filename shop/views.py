from django.http import  JsonResponse,HttpResponse
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = "sk_test_51JVtE7SAdR4FPiJKGBwTOGVhLStluGU8pBujUJ9J82VEnjQYzYrVKy4aHfoVWGmcyCVpmoIBedMiRvhMLu2dzT2s007Jb4bAJU"
YOUR_DOMAIN = 'http://127.0.0.1:8000'

def home(request):
    products = Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products,'home_page': 'active'})

def login_page(request):
    
     if request.user.is_authenticated :
         messages.success(request,"User Alreadylogged in suceesfully")
         return redirect("/")
     else: 
        if request.method == "POST":
            name = request.POST.get('username')
            password= request.POST.get('password')
            print(name,password);
            user = authenticate(request,username=name,password=password)
            print(name,password,user);
            if user is not None:
                login(request,user)
                return redirect("/Collections")
            else:
                messages.warning(request,"Invalid Credentials")
                return redirect("login")
     return render(request,"shop/login.html",{'login_page': 'active'})

def logout_page(request):
    if request.user.is_authenticated :
        logout(request)
        messages.success(request,"User logged out suceesfully")
        redirect("/")
    products = Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart,'cart_page': 'active'})
    else:
        messages.warning(request,"Please Login" )
        return redirect("/")
    
def fav_page(request):
   if request.headers.get('x-requested-with') == "XMLHttpRequest":
       if request.user.is_authenticated:
           data= json.load(request);
           product_id = data["pid"]
           #userId=request.user.id
           product_status= Product.objects.get(id=product_id)
           if product_status:
               if Favourite.objects.filter( user=request.user.id, product_id =product_id):
                   return JsonResponse({"status":"product already added to favourite"}, status=200)
               else:
                    Favourite.objects.create(user=request.user , product_id=product_id)
                    return JsonResponse({"status":"product added to favourite"}, status=200)
       else:
           return JsonResponse({"status":"login to add favourite"}, status=200)
   else:
       return JsonResponse({"status":"Access denied"}, status=200)

def fav_view_page(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request,"shop/favourite.html",{"fav":fav,'fav_page': 'active'})
    else:
        messages.warning(request,"Please Login " )
        return redirect("/")
    
    
    
    
def remove_cart(request,cid):
    cartitems = Cart.objects.get(id=cid)
    cartitems.delete()
    return redirect("/cart")

def remove_fav(request,fid):
    favitems = Favourite.objects.get(id=fid)
    favitems.delete()
    return redirect("/fav_view_page")
    


def add_to_cart(request):
   if request.headers.get('x-requested-with') == "XMLHttpRequest":
       if request.user.is_authenticated:
           data= json.load(request);
           product_qty=data["product_qty"]
           product_id = data["pid"]
           #userId=request.user.id
           product_status= Product.objects.get(id=product_id)
           if product_status:
               if Cart.objects.filter( user=request.user.id, product_id =product_id):
                   return JsonResponse({"status":"product already added to cart"}, status=200)
               else:
                   if product_status.quantity >= product_qty:
                       Cart.objects.create(user=request.user , product_id=product_id, product_qty=product_qty)
                       return JsonResponse({"status":"product added to cart"}, status=200)
                   else:
                       return JsonResponse({"status":"product stock is not available"}, status=200)
       else:
           return JsonResponse({"status":"login to add cart"}, status=200)
   else:
       return JsonResponse({"status":"Access denied"}, status=200)


def register(request):
    form= CustomUserForm();
    if request.method == "POST":
       form= CustomUserForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request,"Account Created Successfully")
           return redirect("/login")
    return render(request,"shop/register.html",{"form":form,"register_page":"active"})

def Collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"Catagory":catagory,"Collections_page":"active"})

def Collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products = Product.objects.filter(catagory__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No Such Catagory found" )
        return redirect("/Collections")


def ProductDetails(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products = Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/productDetails.html",{"products":products})
        else:
            messages.warning(request,"No Such product found" )
            return redirect("collections")
    else:
        messages.warning(request,"No Such Catagory found" )
        return redirect("collections")


def checkout_page(request):
     return render(request,'shop/checkout.html')

#success view
def success(request):
 return render(request,'shop/success.html')

 #cancel view
def cancel(request):
 return render(request,'shop/cancel.html')    

@csrf_exempt
def create_checkout_session(request):
    
  
        if request.user.is_authenticated:
            data= json.load(request);
            Total=data["Total"]
            order=Order(email=" ",paid="False",amount=0,description=" ")
            order.save()

            session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                'name': 'ShopKart',
                },
                'unit_amount': Total * 100,
            },
            'quantity': 1,
            }],
            metadata={
                "order_id":order.id
            },
            mode='payment',
            success_url="http://http://127.0.0.1:8000/success",
            cancel_url="http://http://127.0.0.1:8000/cancel", 
            )

            print(session)
            #ID=order.id
            #order= Order.objects.filter(id=ID).update(email=customer_email,amount=price,paid=True,description=sessionID)
            #order.save()
            return JsonResponse({'id': session.id})
        else:
           return JsonResponse({"status":"login to add cart"}, status=200)
   
    


@csrf_exempt
def webhook(request):
    print("Webhook")
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
         #creating order
        customer_email = session["customer_details"]["email"]
        price = session["amount_total"] /100
        sessionID = session["id"]
        ID=session["metadata"]["order_id"]
        Order.objects.filter(id=ID).update(email=customer_email,amount=price,paid=True,description=sessionID)

    return HttpResponse(status=200)