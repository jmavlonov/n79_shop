from django.forms import ModelForm,Form
from app.models import Comment

class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        # fields = ['id','name','email','message','created_at']
        # fields = '__all__'
        exclude = ('id','product','parent',)

