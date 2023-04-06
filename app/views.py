from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm , CustomerProfileForm

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self, request):
     totalitem = 0
     category = list(Product.objects.all().values_list('category', flat=True))
     object = {}
     choice = {
      'M' : 'Mobile',
      'L': 'Laptop',
      'TW': 'Top Wear',
      'BW': 'Bottom Wear'
     }
     for cat in category:
        object[choice[cat]] = Product.objects.filter(category = cat)
   
     if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
     return render(request, 'app/home.html', {
     'totalitem': totalitem, 'object' : object
     })


def searchAjax(request):
    if request.method == 'GET':
        ProductList = list(Product.objects.all().values_list('title', flat=True)) 
        return JsonResponse(ProductList,safe = False)
   
 
def searchproduct(request):
    if 'searchproducts' in request.GET:
      searchedItem = request.GET['searchproducts']
      product = Product.objects.filter(title__icontains=searchedItem).first()
      if product :
        return redirect("/product-detail/" + str(product.id) )  
      else:
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect(request.META.get("HTTP_REFERER"))

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id), Q(user=request.user)).exists()
        category = Product.objects.filter(category=product.category)
        return render(request, 'app/productdetail.html', {'product': product, 'category': category,
            'item_already_in_cart':item_already_in_cart, 'totalitem' : totalitem})


@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')


@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        totalitem = len(Cart.objects.filter(user=request.user))
        amount = 0.0;
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
            total_amount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount' : total_amount,
                                                          'amount': amount, 'totalitem': totalitem})
        else:
            return render(request, 'app/emptycart.html', {'totalitem': totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        tt = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+= tempamount
            tt += p.quantity
        totalamount = amount + shipping_amount
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : totalamount,
            'tt' : tt
        }
        return JsonResponse(data);





def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        if(c.quantity == 0):
           c.delete()
        else:
           c.save()
        amount = 0.0
        shipping_amount = 70.0
        tt = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            tt += p.quantity
            amount+= tempamount
        totalamount = amount + shipping_amount
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : totalamount,
            'tt' : tt
        }
        return JsonResponse(data);



def remove_cart(request):
  
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        tt = 0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount+= tempamount
            tt += p.quantity
        totalamount = amount + shipping_amount
        data = {
            'amount' : amount,
            'totalamount' : totalamount,
            'tt' : tt
            
        }
        return JsonResponse(data);




def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    totalitem = 0

    def get(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form , 'active': 'btn-primary','totalitem': totalitem})
    def post(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user= usr,name=name, locality=locality, state=state, city=city, phone=phone,
                           email=email,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request,'app/profile.html', {'form': form, 'active' :'btn-primaty', 'totalitem' : totalitem })

@login_required
def address(request):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem })

@login_required
def orders(request):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed' : op, 'totalitem': totalitem})



def mobile(request, data =None):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 if data == None:
     mobiles = Product.objects.filter(category='M')
 elif data == 'OPPO' or data == 'Oneplus':
     mobiles = Product.objects.filter(category='M').filter(brand = data)
 elif data == 'below':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'above':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
 return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})


def laptop(request, data =None):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 if data == None:
     laptops = Product.objects.filter(category='L')
 elif data == 'HP':
     laptops = Product.objects.filter(category='L').filter(brand = data)
 elif data == 'below':
     laptops = Product.objects.filter(category='L').filter(discounted_price__lt=40000)
 elif data == 'above':
     laptops = Product.objects.filter(category='L').filter(discounted_price__gt=40000)
 return render(request, 'app/laptop.html', {'laptops': laptops, 'totalitem': totalitem})



def topwear(request, data =None):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 if data == None:
     topwears = Product.objects.filter(category='TW')
 elif data == 'Concept' or data == 'Siril':
     topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
     topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
 elif data == 'above':
     topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
 return render(request, 'app/topwear.html', {'topwears': topwears, 'totalitem': totalitem})


def bottomwear(request, data =None):
 totalitem = 0
 if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
 if data == None:
     bottomwears = Product.objects.filter(category='BW')
 elif data == 'Kotty' or data == 'Neostreak':
     bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
 elif data == 'above':
     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
 return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears, 'totalitem': totalitem})







class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()

        return render(request, 'app/customerregistration.html',
                      {'form' : form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',
                      {'form': form})

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0.0
 totalitem = 0
 if user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=user))
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if len(add) == 0:
    return redirect("profile")
 elif cart_product:
     for p in cart_product:
         tempamount = (p.quantity * p.product.discounted_price)
         amount += tempamount
     totalamount = amount + shipping_amount

 return render(request, 'app/checkout.html',{'add' : add, 'totalamount' :totalamount
     , 'cart_items': cart_items, 'totalitem': totalitem})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

