from django.contrib import admin
from .models import Product,Customer,Order,OrderDetail
# Register your models here.

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetail)