from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Orders,OrderUpdate
from math import ceil
import json 
# Create your views here.
def index(request):
	return render(request,"user/index.html")

def about(request):
	return render(request,"user/about.html")

def tracker(request):
	return HttpResponse("At tracker")

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
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+" "+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        order = Orders(items_json = items_json,name=name,email=email,address = address,city=city,
                        zip_code=zip_code,state=state, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank = "true" 
        id = order.order_id 
        print("In Post")
        return render(request,'user/checkout.html',{'thank':thank,'id':id})
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
                    response = json.dumps([updates,order[0].items_json],default=str)
                    print([updates,order[0].items_json])
                    print(response)
                return HttpResponse(response) 
            else:    
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request,'user/tracker.html')


def search(request):
	return HttpResponse("At search")
