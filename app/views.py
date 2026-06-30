from django.shortcuts import render,get_object_or_404,redirect
from app.models import Category, Product,Comment
from app.forms import CommentModelForm
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
    comments = product.comments.filter(parent__isnull=True).order_by('-created_at')

    context = {
        'product':product,
        'comments':comments
    }
    return render(request,'app/detail.html',context)


# def add_comment(request,pk):
#     product = get_object_or_404(Product,id = pk)
#     # comments field
#     name = request.POST.get("name","")
#     email = request.POST.get("email","")
#     message = request.POST.get("message","")
#     image = request.FILES.get("image","")
#     rating = request.POST.get("rating","")
#     comment = Comment(name=name,email=email,message=message,file=image,rating=rating)
#     comment.product = product
#     comment.save()
#     return redirect('detail',pk)

def add_comment(request,pk):
    product = get_object_or_404(Product,id = pk)
    if request.method == 'POST':
        form = CommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            parent_id = request.POST.get('parent')
            if parent_id:
                parent = get_object_or_404(Comment,id = parent_id)
                if parent.parent is None or parent.parent.parent is None:
                    comment.parent = parent
            comment.save()
    return redirect('detail',pk)
    

