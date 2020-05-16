from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
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
	return HttpResponse("At checkout")

def search(request):
	return HttpResponse("At search")
