from django.forms import ModelForm,Form
from app.models import Comment, Order,Product

class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        # fields = ['id','name','email','message','created_at']
        # fields = '__all__'
        exclude = ('id','product','parent',)
        
        
class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)


class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('id','created_at','updated_at')
