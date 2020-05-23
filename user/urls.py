from django.urls import path
from . import views 
urlpatterns = [
    path("", views.index,name="PharmHome"),
    path("about/", views.about,name="AboutUs"),
    path("tracker/", views.tracker,name="TrackingStatus"),
    path("order/", views.order,name="Order"),
    path("category/<str:cat>", views.catproducts,name="CatProducts"),
    path("search/", views.search,name="Search"),
    path("productview/<int:myid>", views.productview,name="ProductView"),
    path("checkout/", views.checkout,name="Checkout"),
    path("handlerequest/", views.handlerequest,name="HandleRequest"),
    path("logout/",views.logout,name="Logout")
]
