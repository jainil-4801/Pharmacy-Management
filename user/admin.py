from django.contrib import admin

# Register your models here.
from .models import ProductList,Order,OrderUpd,Cart 

admin.site.register(ProductList)
admin.site.register(Order)
admin.site.register(OrderUpd)
admin.site.register(Cart)