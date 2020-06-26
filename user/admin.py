from django.contrib import admin

# Register your models here.
from .models import ProductList,Order_Table,OrderUpd,Cart_Data 

admin.site.register(ProductList)
admin.site.register(Order_Table)
admin.site.register(OrderUpd)
admin.site.register(Cart_Data)