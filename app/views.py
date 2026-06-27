from django.shortcuts import render,get_object_or_404
from app.models import Category, Product
# Create your views here.


def home(request,category_id : int | None = None):
    
    categories = Category.objects.all()
    products = Product.objects.all()
    
    if category_id is not None:
        products = Product.objects.filter(category = category_id)
    
    context = {
        'categories':categories,
        'products':products
        
    }
    return render(request,'app/home.html',context)



def product_detail(request,pk):
    product = get_object_or_404(Product,id = pk)
    
    context = {
        'product':product
    }
    return render(request,'app/detail.html',context)