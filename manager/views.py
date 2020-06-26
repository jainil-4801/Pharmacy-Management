from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Manager,Supplier
from django.contrib.auth.models import User 
from user.models import ProductList
import warnings

def index(request):
	managers = Manager.objects.all()
	template = loader.get_template("manager/home.html")
	managerdict = {
		'managers' : managers,
	}
	return HttpResponse(template.render(managerdict,request))

def about(request):
	return render(request,"manager/about.html")

def suppliers(request):
	suppliers = Supplier.objects.all()
	template = loader.get_template("manager/supplier.html")
	supplierdict = {
		'suppliers' : suppliers,
	}
	return HttpResponse(template.render(supplierdict,request))

def addproducts(request):
	if request.method == 'POST':
		product=ProductList()
		product.category= request.POST.get('pcategory')
		if product.category=="Homeopathic" or product.category=="Allopathic" or product.category=="Ayurvedic":
			pass
		else:
			# TO DO = CHECK HOMEOPATHIC IF WROMG SHOW IT
			return redirect("/manager/addproducts") 
		product.product_name= request.POST.get('pname')
		product.exp_date= request.POST.get('pexpdate')
		product.desc1= request.POST.get('pdesc1')
		product.desc2= request.POST.get('pdesc2')
		product.price= request.POST.get('pprice')
		product.image= 'user/images/'+request.POST.get('pimg')
		product.discount= request.POST.get('pdiscount')
		product.features= request.POST.get('pfeatures')
		product.use= request.POST.get('puse')
		product.Quantity= request.POST.get('pquantity')
		product.save()
		print(product.image)
		return redirect("/manager/addproducts") 
	else:

		li = [2,3,4,5,6,7,8,9,10,11,12,13]
		context = {
			'li':li,
		}
		template = loader.get_template("manager/addproducts.html")
		return HttpResponse(template.render(context,request)) 

def manageusers(request):
	users = User.objects.all()
	template = loader.get_template("manager/Manageusers.html")
	usersdict = {
		'users' : users,
	}
	return HttpResponse(template.render(usersdict,request))
 
def logout(request):
    return redirect("/logout")