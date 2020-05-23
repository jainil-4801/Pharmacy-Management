from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ProductList,Order,OrderUpd,Cart
from math import ceil
import json 
from django.views.decorators.csrf import csrf_exempt  
from PayTm import Checksum 
from django.contrib.auth.decorators import login_required

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';
# Create your views here.

def index(request):
    try:
        t = Cart.objects.get(user = request.user)
    except Exception as e:
        t = None 
    cart_items = {}
    msg = "All good"
    if t is not None:
        cart_items = t.cart_items
    else:
        msg = "cart_items is empty" 
    params = {"cart_items":json.dumps(cart_items),"msg":msg}
    print(cart_items)
    return render(request,"user/index.html",params)

def about(request):
	return render(request,"user/about.html")

def logout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        try:
            t = Cart.objects.get(user=request.user)
        except Exception as e:
            t = None
        if t is None:
            cart = Cart(user=request.user,cart_items=items_json)
            cart.save()
        else:
            t.cart_items = items_json 
            t.save()
        return redirect("/logout")
    return render(request,"user/logout.html")

@login_required
def order(request):
	return render(request,"user/order.html")

def productview(request,myid):
    product = ProductList.objects.filter(product_id=myid)
    features = product[0].features.split('.')
    return render(request,"user/prodview.html",{'product':product[0],'features':features[:len(features)-1]})

def catproducts(request,cat):
    product = ProductList.objects.filter(category=cat) 
    n = len(product)
    allProdid = []
    for i in product:
        allProdid.append('pr'+str(i.product_id))
    params = {'product':product,'length':n,'allProdid':allProdid}
    return render(request,"user/catproducts.html",params)

@login_required
def checkout(request):
    thank = "false" 
    if request.method =="POST":
        items_json = request.POST.get('itemsJson','')
        name= request.POST.get('name','')
        amount = request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+" "+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        order = Order(user=request.user,items_json = items_json,name=name,email=email,address = address,city=city,
                        zip_code=zip_code,state=state, phone=phone,amount=amount)
        order.save()
        update = OrderUpd(user=request.user,order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank = "true" 
        id = order.order_id 
        return render(request,'user/checkout.html',{'thank':thank,'id':id})
        # request paytm to transfer the amount to your account after payment by user
        # param_dict = {
        #     'MID':'WorldP64425807474247',
        #     'ORDER_ID':str(order.order_id),
        #     'TXN_AMOUNT':str(amount),
        #     'CUST_ID':email,
        #     'INDUSTRY_TYPE_ID':'Retail',
        #     'WEBSITE':'WEBSTAGING',
        #     'CHANNEL_ID':'WEB',
        #     'CALLBACK_URL':'http://127.0.0.1:8000/user/handlerequest/',
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        # return render(request,'user/paytm.html',{'param_dict':param_dict})
    return render(request,'user/checkout.html',{'thank':thank})

@login_required
def tracker(request):
    if request.method=="POST":
        OrderId=request.POST.get('OrderId','')
        email=request.POST.get('email','')
        try:
            order = Order.objects.filter(user=request.user,order_id=OrderId,email=email)
            if len(order)>0:
                update = OrderUpd.objects.filter(order_id=OrderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response) 
            else:    
                return HttpResponse('{"status":"No item"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'user/tracker.html')

def searchMatch(query,item):
    if query in item.desc1.lower() or query in item.desc2.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True  
    return False  


def search(request):
    query = request.GET.get('search')
    allProds = []
    catProds = ProductList.objects.values('category','product_id')
    cats = {item['category'] for item in catProds}
    allProdid = []
    for cat in cats:
        prodtemp = ProductList.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query.lower(),item)]
        n = len(prod)
        if n>0:
            nSlides = n//3+ceil((n/3)-(n//3))
            allProds.append([prod,range(1,nSlides),nSlides])
            for i in prod:
                allProdid.append('pr'+str(i.product_id))
    params = {'msg':"success",'allProds':allProds,'allProdid':json.dumps(allProdid)}
    if len(allProds)==0 or len(query)<4:
        params = {'msg':"Please make sure to enter relavant search query.",'allProdid':json.dumps(allProdid)}
    return render(request,'user/search.html',params)

@csrf_exempt
def handlerequest(request):
    #paytm will send me post reqquest 
    return HttpResponse('done')
    pass