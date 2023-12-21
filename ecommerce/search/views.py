from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
# Create your views here.
def searchprod(request):
    q=""
    product=None
    if(request.method=="POST"):
        q=request.POST['q']
        if q:
            product=Product.objects.filter(Q(name__icontains=q)|Q(desc__icontains=q))
    return render(request,'search.html',{'pro':product,'query':q})
