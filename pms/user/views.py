from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return render(request,"user/index.html")

def about(request):
	return HttpResponse("At about")

def tracker(request):
	return HttpResponse("At tracker")

def order(request):
	return HttpResponse("At order")

def productview(request):
	return HttpResponse("At productview")

def catproducts(request):
	return HttpResponse("At Catproducts")

def checkout(request):
	return HttpResponse("At checkout")

def search(request):
	return HttpResponse("At search")
