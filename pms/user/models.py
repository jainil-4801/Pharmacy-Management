from django.db import models

# Create your models here.
class Product(models.Model):
	product_id = models.AutoField(primary_key=True)
	product_name = models.CharField(max_length=100,default='')
	category = models.CharField(max_length=50,default='')
	desc1 = models.CharField(max_length=300,default='')
	desc2 = models.CharField(max_length=3000,default='')
	exp_date = models.DateField()
	price = models.IntegerField(default=0)
	image = models.ImageField(upload_to="user/images",default="")

	def __str__(self):
		return self.product_name

