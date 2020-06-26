from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ProductList,Order_Table,OrderUpd,Cart_Data
from math import ceil
import json 
from django.views.decorators.csrf import csrf_exempt  
from PayTm import Checksum 
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Sum

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';
# Create your views here.
@login_required 
def index(request): 
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    params = {'total_item':total_item}
    return render(request,"user/index.html",params)

@login_required
def about(request):
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    params = {'total_item':total_item}
    return render(request,"user/about.html",params)

@login_required
def logout(request):
    if request.method=="POST":
        return redirect("/logout")
    return render(request,"user/logout.html")

@login_required
def order(request):
    total_price = 0
    total_cart_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum'] 
    all_items = Cart_Data.objects.filter(user=request.user)
    item_list = []
    for i in all_items:
        cur_prod = ProductList.objects.get(product_id=i.product_id)
        item_tup = (i.product_id,cur_prod.product_name,cur_prod.price*i.quantity,i.quantity)
        item_list.append(item_tup)
        total_price += i.quantity*cur_prod.price
    params = {'item_list':item_list,'total_price':total_price,'total_cart_item':total_cart_item}
    # print(params)
    return render(request,"user/order.html",params)


@login_required
def productview(request,myid):
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    product = ProductList.objects.filter(product_id=myid)
    features = product[0].features.split('.')
    return render(request,"user/prodview.html",{'product':product[0],'features':features[:len(features)-1],'total_item':total_item})

@login_required
def discProducts(request,cat,discount):
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    product = ProductList.objects.filter(category=cat) 
    n = len(product)
    qnt = []
    price = []
    prod_list = []
    for i in product:
        if i.discount<=discount:
            prod_list.append(i)
            try:
                obj = Cart_Data.objects.get(product=i,user=request.user)
                qnt.append(obj.quantity)
            except Cart_Data.DoesNotExist:
                qnt.append(0)
            price.append((i.price,i.price-((i.price*i.discount)//100),((i.price*i.discount)//100),i.discount))
    comb_list = zip(prod_list,qnt,price)
    params = {'comb_list':comb_list,'length':n,'total_item':total_item}
    return render(request,"user/catproducts.html",params)

@login_required
def add_item_cart(request,site,pid):
    prod = ProductList.objects.get(product_id=pid)
    try:
        obj = Cart_Data.objects.get(product=prod,user=request.user)
        obj.quantity+=1 
        obj.save()
    except Cart_Data.DoesNotExist:
        obj = Cart_Data(user=request.user,product=prod,quantity=1)
        obj.save()
    if site=="search":
        return redirect(reverse("Search"))
    return redirect(reverse("CatProducts",args=[prod.category]))

@login_required
def remove_item_cart(request,site,pid):
    prod = ProductList.objects.get(product_id=pid)
    try:
        obj = Cart_Data.objects.get(product=prod,user=request.user)
        obj.quantity-=1
        if obj.quantity == 0:
            obj.delete()
        else:
            obj.save()
    except Cart_Data.DoesNotExist:
        obj = Cart_Data(user=request.user,product=prod,quantity=1)
        obj.save()
    if site=="search":
        return redirect(reverse("Search"))
    return redirect(reverse("CatProducts",args=[prod.category]))

@login_required
def delete_item_cart(request,pid): 
    prod = ProductList.objects.get(product_id=pid)
    obj = Cart_Data.objects.get(product=prod,user=request.user)
    obj.delete()
    return redirect(reverse("Order"))


@login_required
def catproducts(request,cat):
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    product = ProductList.objects.filter(category=cat) 
    n = len(product)
    qnt = [] 
    price = []
    for i in product:
        try:
            obj = Cart_Data.objects.get(product=i,user=request.user)
            qnt.append(obj.quantity)
        except Cart_Data.DoesNotExist:
            qnt.append(0)
        price.append((i.price,i.price-((i.price*i.discount)//100),((i.price*i.discount)//100),i.discount))
    # print(price)
    comb_list = zip(product,qnt,price)
    params = {'comb_list':comb_list,'length':n,'total_item':total_item}
    return render(request,"user/catproducts.html",params)


@login_required
def checkout(request):
    thank = "false" 
    id = None
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
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
        order = Order_Table(user=request.user,items_json = items_json,name=name,email=email,address = address,city=city,
                        zip_code=zip_code,state=state, phone=phone,amount=amount)
        order.save()
        update = OrderUpd(user=request.user,order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank = "true" 
        id = order.order_id
        user_item = Cart_Data.objects.filter(user = request.user)
        user_item.delete()
        # return render(request,'user/checkout.html',{'thank':thank,'id':id,'total_item':total_item})

    total_price = 0
    items = Cart_Data.objects.all()
    
    comb_list = []
    prod_list = []
    quant_list = []
    for i in items:
        prod = ProductList.objects.get(product_id= i.product_id)
        prod_list.append(prod.product_name)
        quant_list.append(i.quantity)
        comb_list.append((prod.product_name,i.quantity))
        total_price = prod.price*i.quantity

    return render(request,'user/checkout.html',{'thank':thank,'id':id,'comb_list':comb_list,'total_price':total_price,'total_item':total_item,'prod_list':prod_list,'quant_list':quant_list})
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
    # return render(request,'user/checkout.html',{'thank':thank})

@login_required
def tracker(request):
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    if request.method=="POST":
        OrderId=request.POST.get('OrderId','')
        email=request.POST.get('email','')
        try:
            order = Order_Table.objects.filter(user=request.user,order_id=OrderId,email=email)
            if len(order)>0:
                update = OrderUpd.objects.filter(order_id=OrderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps({"total_item":total_item,"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response) 
            else:    
                return HttpResponse('{"status":"No item","total_item":total_item}')
        except Exception as e:
            return HttpResponse('{"status":"error","total_item":total_item}')
    return render(request,'user/tracker.html',{'total_item':total_item})


def searchMatch(query,item):
    print(query,item)
    if query in item.desc1.lower() or query in item.desc2.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True  
    return False

query = None 
@login_required
def search(request):
    global query
    t = request.GET.get('search') 
    if t is not None:
        query = t
    allProds = []
    catProds = ProductList.objects.values('category','product_id')
    cats = {item['category'] for item in catProds}
    allProdid = []
    total_item = Cart_Data.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    for cat in cats:
        prodtemp = ProductList.objects.filter(category=cat)
        prod = []
        prod = [item for item in prodtemp if searchMatch(query.lower(),item)]
        n = len(prod)
        if n>0:
            nSlides = n//3+ceil((n/3)-(n//3))
            qnt = []
            price = []
            for i in prod:
                try:
                    obj = Cart_Data.objects.get(product=i,user=request.user)
                    qnt.append(obj.quantity)
                except Cart_Data.DoesNotExist:
                    qnt.append(0)
                price.append((i.price,i.price-((i.price*i.discount)//100),((i.price*i.discount)//100),i.discount))
            allProds.append([zip(prod,qnt,price),range(1,nSlides),nSlides,cat])
    params = {'msg':"success",'allProds':allProds,'total_item':total_item}
    if len(allProds)==0 or len(query)<4:
        params = {'msg':"Please make sure to enter relavant search query.",'allProdid':json.dumps(allProdid)}
    return render(request,'user/search.html',params)

@csrf_exempt
def handlerequest(request):
    #paytm will send me post reqquest 
    return HttpResponse('done')
    pass