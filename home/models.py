from django.db import models
from django.contrib.auth.models import User

class HomeTable(models.Model):
    id=models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    marketingtype = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='images/')
    is_available = models.BooleanField(default=True)
 
class UserInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=11)
    mailid = models.CharField(max_length=100, null=True)
    
    

class ListTable(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id')
    fadvertisement_id = models.ForeignKey(HomeTable, on_delete=models.CASCADE,db_column='fadvertisement_id')
    quantity = models.IntegerField(default=1)

class Payment_history(models.Model):
    id=models.CharField(primary_key=True,max_length=20)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,db_column="user_id")
    datetime = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField(null=True)

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(HomeTable, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

