from django.contrib import admin
from django.utils.html import format_html
from app.models import Category,Product,Comment,Order
# Register your models here.


# admin.site.register(Category)

# admin.site.register(Product)

admin.site.register(Comment)

admin.site.register(Order)

class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'price', 'discount', 'stock', 'image')
    extra = 5
    show_change_link = True


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id','title','products_count')
    inlines = [ProductInline]

    @admin.display(description='Mahsulotlar soni')
    def products_count(self, obj):
        return obj.products.count()
    
    

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['image_preview','name','price','stock']
    list_filter = ['category',]
    search_fields = ['name',]

    @admin.display(description='Rasm')
    def image_preview(self, obj):
        if not obj.image:
            return '—'
        return format_html(
            '<img src="{}" style="height:60px;width:60px;object-fit:cover;border-radius:6px;" />',
            obj.image.url,
        )
        
        