from django.urls import path
from . import views 
urlpatterns = [
    path("", views.index,name="PharmHome"),
    path("about/", views.about,name="AboutUs"),
    path("tracker/", views.tracker,name="TrackingStatus"),
    path("order/", views.order,name="Order"),
    path("catproducts/", views.catproducts,name="CatProducts"),
    path("search/", views.search,name="Search"),
    path("productview/", views.productview,name="ProductView"),
    path("checkout/", views.checkout,name="Checkout"),
    
    
]
