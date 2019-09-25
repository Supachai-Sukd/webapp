from django.db import models
from django.contrib.auth.models import User
 
# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = (
        ("IT", "IT & Gadget"),
        ("EL", "Electronics"),
        ("FA", "Fashion")
    )
    
    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=500)
    price = models.FloatField()
    photo = models.ImageField(upload_to='products')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name
 
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.CharField(max_length=500)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
 
    def __str__(self):
        return self.user.username
 
class Order(models.Model):
    NEW = 1
    PAID = 2
    DELIVERED = 3
 
    STATUS_CHOICES = (
        (NEW, "รอการชำระเงิน"),
        (PAID, "ชำระเงินแล้วรอการจัดส่ง"),
        (DELIVERED, "จัดส่งสินค้าแล้ว")
    )
 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=500)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
 
    def __str__(self):
        return '%s (%s)' % (str(self.id), str(self.created_at))
 
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.DecimalField(max_digits=18, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return '%s x %s' % (self.product.name, str(self.quantity))
    
    
    

    
