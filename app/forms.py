from django.forms import ModelForm,Form
from app.models import Comment, Order

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

