from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index,name="manHome"),
    path("about/",views.about,name="about"),
    path("suppliers/",views.suppliers,name="supplierslist"),
    path("addproducts/",views.addproducts,name="addproducts"),
    path("manageusers/",views.manageusers,name="addproducts"),
    path("logout/",views.logout,name="Logout")
]
