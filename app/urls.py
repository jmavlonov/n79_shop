from django.urls import path,include
from app.views import home,product_detail,add_comment,order_view,create_product,delete_product

urlpatterns = [
    path('home/',home,name='home'),
    path('category/<int:category_id>/products/',home,name='products_of_category'),
    path('detail/<int:pk>',product_detail,name='detail'),
    path('add-comment/<int:pk>/',add_comment,name='add_comment'),
    path('add-order-view/<int:pk>/',order_view,name='order_view'),
    path('add-product/',create_product,name='create_product'),
    path('delete-product/<int:pk>/',delete_product,name='delete_product')
    
]
