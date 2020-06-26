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
    path("logout/",views.logout,name="Logout"),
    path("discount/<str:cat>/<int:discount>",views.discProducts,name="DiscountProducts"),
    path("<str:site>/add/<int:pid>",views.add_item_cart,name="add_item_cart"),
    path("<str:site>/sub/<int:pid>",views.remove_item_cart,name="remove_item_cart"),
    path("del/<int:pid>",views.delete_item_cart,name="delete_item_cart"),
       
]
