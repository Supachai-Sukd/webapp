from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Order,OrderDetail
from decimal import Decimal
# Create your views here.

def home(request):
    products = Product.objects.filter(status=True)
    
    return render(request,'index.html',{"products" : products})

def product_detail(request,id):
    product = Product.objects.get(id=id)
    tmp_quantity = 0
    #เป็น method post และเช็คว่า login หรือเปล่า ถ้า login ให้ทำต่อ
    if request.method == "POST" and not request.user.is_anonymous:
        try:
            #ข้างล่างนี้เป็น query set และเป็น order ของ customer ที่ login อยู่ สถานะเป็นออเดอร์ใหม่
            order = Order.objects.get(customer = request.user.customer, status = Order.NEW)
            #ข้างล่างแปลว่า ถ้าไม่มี Order เราจะสร้าง order ใหม่
        except Order.DoesNotExist:
            #ข้างล่างเป็น query set
            order = Order.objects.create(
                customer = request.user.customer,
                status = Order.NEW,
                total = 0
            )
        #ขั้นตอนต่อไปเราจะดึง order detail ของ order นั้นมาถ้ามี
        try:
            #เพื่อที่จะเช็คว่ามีสินค้านี้ในตะกร้าหรือยัง
            order_detail = OrderDetail.objects.get(order=order, product=product)
            #ถ้ามีแล้วเราจะได้เพิ่มจำนวนเข้าไป
            tmp_quantity = order_detail.quantity
            #แต่ถ้าไม่มีเราจะสร้าง order detail ใหม่
        except OrderDetail.DoesNotExist:
            order_detail = OrderDetail.objects.create(
                order=order,
                product=product,
                quantity=0,
                sub_total=0
            )
        
        #ข้างล่างนี้เป็นการคำนวณออเดอร์สินค้าในวงเล็บคือเป็นสินค้าเก่า tmp คือสินค้าที่กดมาใหม่ทีหลัง
        order_detail.quantity = int(request.POST['quantity']) + tmp_quantity

        order_detail.sub_total = Decimal(product.price) * Decimal(int(request.POST['quantity']) + tmp_quantity)
        order_detail.save()
 
        tmp_total = 0
        #เราใช้คำสั่ง for loop เพื่อหา total
        for tmp_order_detail in order.order_details.all():
            #คือเอา sub total มา + กับทั้งหมด
            #ถ้า order มากกว่า 1 เราต้องเก็บค่าตัวแปรไว้ที่ tmp_total ก่อนเสร็จแล้วก็เอา tmp มา +กับ sub total
            #ของสินค้าอีกอันนึง ของ order detail อีกอันนึงเพื่อให้ได้ผลรวมที่ถูกต้อง 
            tmp_total += tmp_order_detail.sub_total
        
        order.total = tmp_total
        order.save()
 
        return redirect('my_cart')
            
    return render(request, 'product_detail.html', {"product" : product })

def product_search(request):
    if 'product_search' in request.GET:
        products = Product.objects.filter(name__contains = request.GET['product_search'])
        return render(request, 'index.html', {"products" : products})
    else:
        return redirect('home')

#ก็คือเอาดึง order ของ user ที่ login อยู่แล้วก็สถานะเป็น new
def my_cart(request):
    order = Order.objects.get(customer = request.user.customer,status = Order.NEW)
    #ส่ง พารามิเตอร์ชื่อออเดอร์ และก็ส่ง  order ของเราเข้าไป
    return render(request,'my_cart.html',{"order" : order})
    
def delete_order_detail(request,id):
    try:
        #ขั้นแรกเราก็จะเช็คว่า order detail นี้ที่ส่งเข้ามามีอยู่จริงไหม
        #except OrderDetail.DoesNotExist เจ้า DoesNot เนี่ยคือแปลว่าถ้าไม่เจอ
        order_detail = OrderDetail.objects.get(id=id)
    #ข้างล่างคือถ้าไม่เจอ order detail ให้ทำคำสั่งล่างต่อไปคือกลับไปที่ my_cart
    #redirect มันเหมือนกลับถ้าไม่เจออะไรแล้วให้ย้อนกลับไปตรง url ที่ตั้งไว้ มักจะใช้กับ url
    except OrderDetail.DoesNotExist:
        return redirect('my_cart')
    #แต่ถ้าเจอ method POST ให้ทำข้างล่างต่อไป คือ delete ทันที
    if request.method == "POST":
    #ข้างล่างนี้คือ รูปแบบ query set
        order_detail.delete()
        #หลัง delete เสร็จเราก็จะ get order ของ user คนที่ login อยู่
        #และ status new นั้นเพื่อมาคำนวณหาราคาสินค้าตะกร้าสินค้าว่ามีมูลค่าเท่าไหร่
        #เนื่องจากว่าลูกค้าจะสามารถมี order status new ได้แค่ 1
        order = Order.objects.get(customer=request.user.customer,status=Order.NEW)
        tmp_total = 0
        #เราใช้คำสั่ง for loop เพื่อหา total
        for tmp_order_detail in order.order_details.all():
            #คือเอา sub total มา + กับทั้งหมด
            #ถ้า order มากกว่า 1 เราต้องเก็บค่าตัวแปรไว้ที่ tmp_total ก่อนเสร็จแล้วก็เอา tmp มา +กับ sub total
            #ของสินค้าอีกอันนึง ของ order detail อีกอันนึงเพื่อให้ได้ผลรวมที่ถูกต้อง 
            tmp_total += tmp_order_detail.sub_total
        
        order.total = tmp_total
        order.save()
        #หลังจากที่คำนวณเสร็จด้วย loop ด้วยอะไรแล้วเราก็จะ return ไปที่ my_cart
        return redirect('my_cart')
    
    return render(request,'delete_order_detail.html',{"order_detail" : order_detail})
    
