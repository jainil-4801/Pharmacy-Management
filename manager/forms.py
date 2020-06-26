from django import forms 
from user.models import ProductList 

class ProductForm(forms.ModelForm):

	class Meta():
		model = ProductList
		exclude = ('product_id',)

