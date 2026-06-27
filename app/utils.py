def product_image_path(instance, filename):
    # instance - Product objecti
    # filename - yuklangan fayl nomi
    category_title = instance.category.title.lower().replace(' ', '_')
    return f'products/{category_title}/{filename}'
