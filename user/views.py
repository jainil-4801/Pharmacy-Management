from django.shortcuts import render
from django.http import HttpResponse
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

def catproducts(request):
	return render(request,"user/catproducts.html")

def checkout(request):
	return HttpResponse("At checkout")

def search(request):
	return HttpResponse("At search")
