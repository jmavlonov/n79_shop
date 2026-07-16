from django.shortcuts import render,get_object_or_404,redirect
from app.models import Category, Product,Comment
from app.forms import CommentModelForm,OrderModelForm,ProductModelForm
from django.contrib import messages
from django.db.models import Q
from app.utils import product_price_filter
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce


# Create your views here.


def home(request,category_id : int | None = None):
    search_query = request.GET.get("q","")
    filter_type = request.GET.get("filter_type","")
    categories = Category.objects.all() # select * from categories;
    products = Product.objects.annotate(avg_comment = Coalesce(Avg('comments__rating'), Value(0.0)))

    if category_id is not None:
        products = products.filter(category = category_id)

    if search_query:
        products = products.filter(Q(name__icontains = search_query) | Q(description__icontains = search_query))

    
    products = product_price_filter(filter_type,products)


    context = {
        'categories':categories,
        'products':products,
    }
    return render(request,'app/home.html',context)



def product_detail(request,pk):
    product = get_object_or_404(Product,id = pk)
    # comments = product.comments.filter(parent__isnull=True).order_by('-created_at')
    comments = product.comments.all().order_by('-created_at')
    related_products = Product.objects.filter(category = product.category).exclude(id=product.id)
    
    context = {
        'product':product,
        'comments':comments,
        'related_products':related_products,
        
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
    

def order_view(request,pk):
    product = get_object_or_404(Product,id = pk)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.stock < order.quantity:
                # add message warning info
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Buyurtmalar soni Skladdagi productlar sonidan ortiq"
                )
                print('-----------------')

            else:
                product.stock -= order.quantity
                product.save()
                order.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{order.id} Buyurtma muvaffaqiyatli amalga oshirildi."
                )
                print('++++++++++++++')
                # add message success info
        else:
            messages.error(request, "Telefon raqamini to'g'ri kiriting: +998XXXXXXXXX")

    return redirect('detail',pk)

def create_product(request):
    
    if request.method == "POST":
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductModelForm()
        
    context = {
        'form':form
    }
        
    
    return render(request,'app/add-product.html',context=context)