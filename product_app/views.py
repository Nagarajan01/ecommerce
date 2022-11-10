from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Sum
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from django.conf import settings

from .models import *
import json
import stripe
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_PRIVATE_KEY

class SuccessView(TemplateView):
    template_name = "accounts/success.html"

class CancelView(TemplateView):
    template_name = "accounts/success.html"

def checkout(request):
    order = Order.objects.filter(user=request.user).last()
    order_items = order.items.all()
    prices =[]

    for item in order_items:
        product = stripe.Product.create(
            name=item.product.title, description=item.product.title, 
            images = [])
        price = stripe.Price.create(product=product.id, unit_amount=int(
            item.product.price + int(18/100 * item.product.price))*100, currency='inr')
        prices.append(price.id)

    line_items=[]
    for item, price in zip(order_items,prices):
            line_items.append({'price':price,'quantity':item.quantity}),
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=line_items,
    metadata={
        'order':order.id
    },
    mode='payment',
    success_url='http://127.0.0.1:8000/success/',
    cancel_url='http://127.0.0.1:8000/cancel/'
    )
    return redirect(session.url)

mylist1 = []
mylist2 = []
mylist3 = []
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    mypayload = request.body.decode("utf-8")
    a = json.loads(payload)  #>>> in this variable, I can render three type("charge.succeeded", "checkout.session.completed", "payment_intent.succeeded")
    if a['type']=="charge.succeeded": 
        b = a["data"]["object"]["outcome"]["seller_message"]
        c = a["data"]["object"]["id"]
        mylist1.append(b)
        mylist1.append(c)
    
    if a['type']=="checkout.session.completed":
        c = a['data']['object']['metadata']['order']
        mylist2.append(c)

    if len(mylist1)==2 and len(mylist2)==1:
        ['Payment complete.', 'ch_3M2BLtSAnvLl9E2S107SmFNO']
        ['42']
        if mylist1[0] =="Payment complete.":
            Payment_Detail.objects.get_or_create(
            transaction_id = mylist1[1], order=Order.objects.get(id = int(mylist2[0])), payment_status= mylist1[0])
    if a['type']=='charge.failed':
        b = a["data"]["object"]["outcome"]["seller_message"]
        c = a["data"]["object"]["id"]
        mylist3.append(b)
        mylist3.append(c)
        print(mylist2)
        print(mylist3)
        ob = Order.objects.all().values('id').last()
        Payment_Detail.objects.get_or_create(
        transaction_id = mylist3[1], order=Order.objects.get(id = int(ob['id'])), payment_status= b)
    return HttpResponse(status=200)
    


def loginPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(request.user)
            return redirect('product_app:SearchResultsView')
        else:
            form = AuthenticationForm()
            messages.info(request, 'username or password is incorrect')
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('product_app:login')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('product_app:login')
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


class Lists(ListView):
    model = Item
    template_name = "accounts/show_products.html"
    context_object_name = 'form'
    queryset = Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Lists, self).get_context_data(**kwargs)
        return context



from datetime import date 
import datetime
class listjson(ListView):
    model = Item  
    def render_to_response(self, context, *args, **kwargs):
        detail_Mark_json = Item.objects.all().values()
        a = []
        for i in detail_Mark_json:
            x = date.today() 
            y = x.strftime("%d, %B, %Y")    
            z = y.split(", ")
            z[1] = z[1][0:3]
            i["date"] = x
            a.append(i)
        data = json.dumps(a, default=str, indent=1)
        print(type(data))
        return HttpResponse(data, content_type='application/json')

@login_required
class index(ListView):
    template_name = "accounts/index.html"
    model = Item


@login_required(login_url='accounts/login/')
def add_to_cart(request, **kwargs):
    query = Item.objects.get(id=kwargs['id'], in_stock=True)
    ncart = CartItem.objects.create(user=request.user, product=query)
    if 'discount_price' != 'null':
        mytprice = CartItem.objects.annotate(
            price=Sum(F('product__discount_price')*F('quantity'))).values()
    mytprice = CartItem.objects.annotate(price=Sum(F('product__price')*F('quantity'))).values()
    ncart.save()
    mylist = []     
    for i in mytprice:
        mylist.append(i)
    data = json.dumps(mylist, default=str, indent=1)
    print(type(data))
    return HttpResponse(data, content_type='application/json')


from datetime import date 
import datetime
class view_cart_json(ListView):

    model = CartItem
    def render_to_response(self, context, *args, **kwargs):

        ob = CartItem.objects.filter(
            user=self.request.user, ordered=False).order_by('product__title').values('product_id', 'quantity')
        mylist = []     
        for i in ob:
            ob_p = Item.objects.filter(id=i['product_id'])
            mylist.append(ob_p[0])
        data = json.dumps(mylist, default=str, indent=1)
        print(type(data))
        return HttpResponse(data, content_type='application/json')


class view_cart(ListView):
    model = CartItem
    template_name = "accounts/cart_page.html"
    context_object_name = 'form'

    def get_queryset(self, **kwargs):
        ob = self.model.objects.filter(
            user=self.request.user, ordered=False).order_by('product__title').values('product_id', 'quantity')
        mylist = []     
        for i in ob:
            ob_p = Item.objects.filter(id=i['product_id'])
            mylist.append(ob_p[0])
        return mylist


@login_required(login_url='accounts/login/')
def cart_update(request):
    product_id = request.POST.get('id')
    product_price = request.POST.get('price')
    product_quantity = request.POST.get('quantity')
    cart_item = CartItem.objects.filter(product=product_id)
    object = cart_item[0]
    object.quantity = (product_quantity)
    print(product_quantity)
    object.total = int(object.quantity) * int(float(product_price))
    print(object.quantity)
    object.save()
    return redirect('product_app:view_cart')


@login_required(login_url='accounts/login/')
def order_results(request):
    vaf = CartItem.objects.filter(user=request.user)
    vaf.update(ordered = True)
    b = Order.objects.create(user=request.user)
    b.items.add(*CartItem.objects.filter(user=request.user))
    my_total = Order.objects.filter(
        user=request.user).aggregate(Sum('items__product__price'))
    b.total = my_total['items__product__price__sum']
    b.save()
    
    return redirect('product_app:order_view')


@login_required(login_url='accounts/login/')
def order_view(request):
    template = "accounts/order_page.html"
    cart_list = CartItem.objects.filter(user=request.user)
    order_list = Order.objects.all().values().last()
    my_total = CartItem.objects.filter(Q(user=request.user) & Q(ordered=True)).exclude(status='Failed').aggregate(Sum('total'))['total__sum']
    mylist = []     
    '''for i in cart_list:
        mylist.append(i)'''
    if my_total is None:
            new_cart_list = CartItem.objects.filter(user=request.user, ordered = True)
            new_total = 0
            new_price = new_total
            new_tax = 18/100 * new_price
            total_price = new_price + new_tax
            context = {'cart_list': cart_list, 'my_total': new_price, 'tax': new_tax, 'total_price':total_price, 'product':order_list}
            return render(request, template, context)            
    price = my_total 
    if price is None:
        return render(request, "accounts/order_page.html", {"message": "You have no orders"})
    new_tax = 18/100 * price    
    total_price = price + new_tax
    context = {'cart_list': cart_list, 'my_total': price, 'tax': new_tax, 'total_price':int(total_price), 'order':order_list}
    return render(request, template, context)
    
# >Below code is json convertions,
'''
data = json.dumps(context, default=str, indent=1)
print(type(data))
return HttpResponse(data, content_type='application/json')'''
'''
data = json.dumps(context, default=str, indent=1)
print(type(data))
return HttpResponse(data, content_type='application/json')'''


@login_required(login_url='accounts/login/')
def get_queryset(request):
    template_name = "accounts/search_results.html"
    query = request.GET.get('your_name')
    if query is not None:
        form = Item.objects.filter((Q(brand__brand__icontains=query) | Q(
            title__icontains=query)) & Q(in_stock=True)).values()
        mylist = []
        for i in form:
            mylist.append(i)
        ob = Wishlist.objects.all().values('wished_item_id')
        my_list = []
        for i, index in enumerate(list(ob)):
            my_list.append(index['wished_item_id'])
        context = {'object_list': mylist, 'favorites': my_list}

        data = json.dumps(context, default=str, indent=1)
        print(type(data))
        return HttpResponse(data, content_type="application/json")
    else:
        form = Item.objects.filter(in_stock=True)
        ob = Wishlist.objects.all().values('wished_item_id')
        my_list = []
        for i, index in enumerate(list(ob)):
            my_list.append(index['wished_item_id'])
        context = {'object_list': form, 'my_list': my_list}
        return render(request, template_name, context)

# >Below code is json convertions,
'''
data = json.dumps(context, default=str, indent=1)
print(type(data))
return HttpResponse(data, content_type="application/json")'''


@login_required(login_url='accounts/login/')
def add_to_wishlist(request, **kwargs):
    query = Item.objects.get(id=kwargs['id'])
    created = Wishlist.objects.get_or_create(
        user=request.user, wished_item=query)
    return redirect('product_app:SearchResultsView')


@login_required(login_url='accounts/login/')
def removewishlist(request, **kwargs):
    query = Item.objects.get(id=kwargs['id'])
    created = Wishlist.objects.filter(
        user=request.user, wished_item=query).delete()
    return redirect('product_app:SearchResultsView')


@login_required(login_url='accounts/login/')
def updateorder(request):
    prd_id = request.POST.get('id')
    query = CartItem.objects.get(id=prd_id)
    query.status = "Failed"
    query.save()
    return redirect('product_app:order_results')


class view_wishlist(ListView):
    model = Wishlist
    template_name = "accounts/wishlists.html"
    context_object_name = 'form'

    def get_queryset(self, **kwargs):
        ob = self.model.objects.filter(
            user=self.request.user).values('wished_item')
        mylist = []
        for i in ob:
            ob_p = Item.objects.filter(id=i['wished_item'])
            mylist.append(ob_p[0])
        return mylist

