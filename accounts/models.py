from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGOTRIES =   (
                        ('داخلي','داخلي'),
                        ('خارجي','خارجي'),
                        )
                        
    name= models.CharField(max_length=200, null=True)
    price= models.FloatField(null=True)
    category= models.CharField(max_length=200, null=True, choices=CATEGOTRIES)
    desc= models.CharField(max_length=200,null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    CATEGOTRIES =   (
                        ('متأخر','متأخر'),
                        ('للتوصيل','للتوصيل'),
                        ('تم التوصيل','تم التوصيل'),
                        )
    customer= models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product= models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=CATEGOTRIES)
    note = models.CharField(max_length=200, null=True)
   

class OrderHistory(models.Model):

    version_num = models.AutoField(primary_key=True)
    Order = models.ForeignKey(Order, null=True, on_delete= models.SET_NULL,related_name='thorders')
    customer= models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product= models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True)
    note = models.CharField(max_length=200, null=True)
