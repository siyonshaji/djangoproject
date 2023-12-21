from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Order,Account


# Create your views here.
def cartview(request):
    sum=0
    u=request.user
    try:
        cart=Cart.objects.filter(user=u)
        for i in cart:
            sum+=i.quantity*i.product.price
    except:
        pass
    return render(request,'cart.html',{'c':cart,'total':sum})

@login_required
def cart(request,p):
    pro=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=pro,user=u)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
        cart.save()
    except:
        cart=Cart.objects.create(product=pro,user=u,quantity=1)
        cart.save()

    return cartview(request)
def minus(request,p):
    pro=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=pro,user=u)
        if(cart.quantity>1):
            cart.quantity-=1

            cart.save()
        else:
            cart.delete()
    except:
        pass
    return cartview(request)

def delete(request,p):
    pro=Product.objects.get(name=p)
    u=request.user
    try:
        cart=Cart.objects.get(product=pro,user=u)

        cart.delete()
    except:
        pass
    return cartview(request)

def orderform(request):
    if(request.method=="POST"):
        ad=request.POST['ad']
        ph=request.POST['ph']
        an=request.POST['an']
        u=request.user
        cart=Cart.objects.filter(user=u)
        total=0
        for i in cart:
            total+=i.quantity*i.product.price
        ac=Account.objects.get(accnum=an)
        if(ac.amount >= total):
            ac.amount-=total
            ac.save()
            for i in cart:
                o=Order.objects.create(user=u,product=i.product,phone=ph,address=ad,noofitems=i.quantity,order_status="paid")
                o.save()
                i.product.stock-=i.quantity
                i.product.save()
            cart.delete()
            msg="order placed successfully"
            return render(request,'orderdetails.html',{'m':msg})
        else:
            msg="Insufficient balance in your account"
            return render(request,'orderdetails.html',{'m':msg})
    return render(request,'orderform.html')
def orderview(request):
    u=request.user
    a=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'a':a})
