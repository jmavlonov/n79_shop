from django.urls import path,include
from app.views import home,product_detail

urlpatterns = [
    path('home/',home,name='home'),
    path('category/<int:category_id>/products/',home,name='products_of_category'),
    path('detail/<int:pk>',product_detail,name='detail')
    
]
