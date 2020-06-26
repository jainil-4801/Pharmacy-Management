from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Manager,Supplier
from django.contrib.auth.models import User 
from user.models import ProductList
import warnings
from manager.forms import ProductForm



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


def addprods(request):
	if request.method == "POST":
		product_form = ProductForm(data = request.POST)

		if product_form.is_valid():
			product = product_form.save(commit=False)

			if 'image' in request.FILES:
				product.image = request.FILES['image']

			product.save()
		else:
			print(product_form.errors)
	else:
		product_form = ProductForm()

	return render(request,"manager/addprods.html",{'product_form':product_form})




def addproducts(request):
	if request.method == 'POST':
		product = ProductList()
		product.product_name = request.POST.get('pname')
		product.category = request.POST.get('category')
		product.exp_date = request.POST.get('pexpdate')
		product.desc1 = request.POST.get('pdesc1')
		product.desc2 = request.POST.get('pdesc2')
		product.price = request.POST.get('pprice')
		# May Work Don't Know.....
		product.image = request.FILES['pimage']
		product.discount = request.POST.get('pdiscount')
		product.features = request.POST.get('pfeatures')
		product.use = request.POST.get('puse')
		product.Quantity = request.POST.get('pquantity')
		product.save()

		print(product.product_name)
		print(product.category)
		print(product.exp_date)
		print(product.desc1)
		print(product.desc2)
		print(product.price)
		print(product.image)
		print(product.discount)
		print(product.features)
		print(product.use)
		print(product.Quantity)				
	return render(request,"manager/addproducts.html") 
	# else:

	# 	li = [2,3,4,5,6,7,8,9,10,11,12,13]
	# 	context = {
	# 		'li':li,
	# 	}
	# 	template = loader.get_template("manager/addproducts.html")
	# 	return HttpResponse(template.render(context,request)) 

def manageusers(request):
	users = User.objects.all()
	template = loader.get_template("manager/Manageusers.html")
	usersdict = {
		'users' : users,
	}
	return HttpResponse(template.render(usersdict,request))
 
def logout(request):
    return redirect("/logout")