def product_image_path(instance, filename):
    # instance - Product objecti
    # filename - yuklangan fayl nomi
    category_title = instance.category.title.lower().replace(' ', '_')
    return f'products/{category_title}/{filename}'



def product_price_filter(filter_type,products = None):
    if filter_type == "expensive":
        products = products.order_by("-price")

    elif filter_type == "cheap":
        products = products.order_by("price")
        
    return products