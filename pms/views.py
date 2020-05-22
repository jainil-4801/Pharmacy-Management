from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth 
from user.models import Cart 

# Create your views here.
def login(request):
	params = {'msg':'All good'}
	if request.method=="POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect("/user")
		else:
			params = {'msg':"Invalid Credentials"}
	return render(request,"login.html",params)

def register(request):
	params = {'msg':'All good'}
	if request.method=="POST":
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		username = request.POST["username"]
		password1 = request.POST["password1"]
		password2 = request.POST["password2"]
		if password1==password2:
			if User.objects.filter(username=username).exists():
				params = {'msg':'username already exists'}
			else:
				user = User(first_name=first_name,last_name=last_name,username=username,password=password1)
				user.save()
				return redirect("/login")
		return redirect("/user")
	else:
		return render(request,'register.html',params)
def logout(request):
	auth.logout(request)
	return redirect("/login")
