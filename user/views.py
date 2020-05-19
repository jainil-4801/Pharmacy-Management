from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Orders,OrderUpdate
from math import ceil
import json 
from django.views.decorators.csrf import csrf_exempt  
from PayTm import Checksum 
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';
# Create your views here.
def index(request):
	return render(request,"user/index.html")

def about(request):
	return render(request,"user/about.html")

def order(request):
	return render(request,"user/order.html")

def productview(request):
	return HttpResponse("At productview")

def catproducts(request,cat):
	product = Product.objects.filter(category=cat)
	n = len(product)
	params = {'product':product,'length':n}
	return render(request,"user/catproducts.html",params)

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
        order = Orders(items_json = items_json,name=name,email=email,address = address,city=city,
                        zip_code=zip_code,state=state, phone=phone,amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
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

def tracker(request):
    if request.method=="POST":
        OrderId=request.POST.get('OrderId','')
        email=request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=OrderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=OrderId)
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
    catProds = Product.objects.values('category','product_id')
    cats = {item['category'] for item in catProds}
    allProdid = []
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
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