from .models import Customer

#ความหมายด้านล่างนี้คือถ้าไม่เจอ Customer ให้สร้างใหม่เลย
def save_customer(backend,user,response,*args,**kwargs):
    try:
        customer = Customer.objects.get(user_id=user.id)
    except Customer.DoesNotExist:
        customer = Customer(user_id=user.id)
    #ถ้้า backend เป็น facebook ให้สร้างเป็น
    if backend.name == 'facebook':
        customer.email = response.get('email')
        #รูป facebook เก็บเป็น path
        customer.photo = 'http://graph.facebook.com/%s/picture?type=large'% response.get('id')
        customer.save()

        