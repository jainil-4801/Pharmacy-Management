from django.db import models
from user.models import ProductList

class Manager(models.Model):

    Firstname = models.CharField(max_length=20)
    Lastname = models.CharField(max_length=20)
    Username = models.CharField(max_length=50,primary_key=True)
    Email = models.CharField(max_length=80)

    def __str__(self):
        return self.Firstname + " " + self.Lastname

class Supplier(models.Model):
    Firstname = models.CharField(max_length=20)
    Lastname = models.CharField(max_length=20)

    Email = models.CharField(max_length=80,primary_key=True)

    def __str__(self):
        return self.Firstname + " " + self.Lastname

