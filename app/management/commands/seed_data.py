import random
from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from app.models import Category, Product


# Har bir kategoriya uchun: rang (gradient uchun) va mahsulotlar ro'yxati
CATEGORIES = {
    'Smartfonlar': {
        'color': ((253, 126, 20), (232, 89, 12)),
        'products': [
            ('iPhone 15 Pro Max', 16_990_000, 'Titan korpus, A17 Pro chip, 256GB xotira.'),
            ('Samsung Galaxy S24 Ultra', 15_500_000, 'S Pen bilan, 200MP kamera, 512GB.'),
            ('Xiaomi 14 Pro', 9_200_000, 'Leica optikasi, Snapdragon 8 Gen 3.'),
            ('Google Pixel 8', 7_800_000, 'Toza Android, eng yaxshi kamera dasturi.'),
            ('Redmi Note 13 Pro', 3_400_000, 'Byudjet segmentidagi eng kuchli variant.'),
        ],
    },
    'Noutbuklar': {
        'color': ((13, 110, 253), (10, 88, 202)),
        'products': [
            ('MacBook Pro 16 M3', 28_500_000, 'M3 Pro chip, 18GB RAM, 512GB SSD.'),
            ('MacBook Air 13 M2', 14_200_000, 'Yengil, fansiz, 18 soat batareya.'),
            ('Dell XPS 15', 19_800_000, 'OLED displey, RTX 4050, 32GB RAM.'),
            ('Lenovo ThinkPad X1', 17_300_000, 'Biznes uchun, klaviaturasi ideal.'),
            ('Asus ROG Strix G16', 15_900_000, 'Gaming noutbuk, RTX 4060, 165Hz.'),
        ],
    },
    'Muzlatgichlar': {
        'color': ((32, 201, 151), (25, 135, 84)),
        'products': [
            ('Samsung RB37 No Frost', 8_900_000, '367 litr, No Frost, inverter kompressor.'),
            ('LG GC-B247 Door Cooling', 11_400_000, 'Door Cooling+, 10 yil kafolat.'),
            ('Artel HD 316 FN', 4_200_000, 'O‘zbekiston ishlab chiqarishi, 316 litr.'),
            ('Bosch KGN39', 13_700_000, 'VitaFresh, past shovqin darajasi.'),
            ('Shivaki HD 360', 5_100_000, 'Ikki kamerali, energiya tejamkor.'),
        ],
    },
    'Changyutgichlar': {
        'color': ((111, 66, 193), (89, 50, 160)),
        'products': [
            ('Dyson V15 Detect', 9_600_000, 'Lazerli chang detektori, simsiz.'),
            ('Xiaomi Robot Vacuum S10', 4_300_000, 'Robot changyutgich, LiDAR navigatsiya.'),
            ('Samsung VC18M', 2_100_000, 'Sim bilan, 1800W, HEPA filtr.'),
            ('Philips XB2125', 1_750_000, 'Kompakt, 900W, sumkasiz.'),
        ],
    },
    'Televizorlar': {
        'color': ((220, 53, 69), (176, 42, 55)),
        'products': [
            ('Samsung QLED 65" Q80C', 14_800_000, '4K QLED, 120Hz, Tizen OS.'),
            ('LG OLED 55" C3', 16_200_000, 'OLED evo panel, HDMI 2.1.'),
            ('Artel 43" Smart', 3_200_000, 'Full HD, Android TV.'),
            ('Xiaomi TV A2 50"', 4_900_000, '4K HDR10, Google TV.'),
        ],
    },
    'Quloqchinlar': {
        'color': ((255, 193, 7), (224, 168, 0)),
        'products': [
            ('AirPods Pro 2', 3_100_000, 'Faol shovqin bostirish, USB-C.'),
            ('Sony WH-1000XM5', 4_500_000, 'Sinfdagi eng yaxshi ANC.'),
            ('JBL Tune 770NC', 1_400_000, '70 soat batareya, simsiz.'),
            ('Marshall Major IV', 2_200_000, 'Retro dizayn, 80 soat ishlaydi.'),
        ],
    },
}

FONT_PATHS = [
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]


def load_font(size):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_image(name, category_title, colors, size=800):
    """Mahsulot uchun gradientli placeholder rasm yasaydi."""
    top, bottom = colors
    image = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(image)

    # Vertikal gradient
    for y in range(size):
        ratio = y / size
        draw.line(
            [(0, y), (size, y)],
            fill=tuple(int(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3)),
        )

    # Kategoriya nomi (yuqorida, xira)
    cat_font = load_font(30)
    draw.text((size / 2, 90), category_title.upper(), font=cat_font,
              fill=(255, 255, 255, 180), anchor='mm')

    # Mahsulot nomi — uzun bo'lsa so'zlab qatorlarga bo'lamiz
    font = load_font(52)
    words, lines, current = name.split(), [], ''
    for word in words:
        candidate = f'{current} {word}'.strip()
        if draw.textlength(candidate, font=font) > size - 120:
            lines.append(current)
            current = word
        else:
            current = candidate
    lines.append(current)

    start_y = size / 2 - (len(lines) - 1) * 34
    for i, line in enumerate(lines):
        draw.text((size / 2, start_y + i * 68), line, font=font,
                  fill=(255, 255, 255), anchor='mm')

    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=88)
    return buffer.getvalue()


class Command(BaseCommand):
    help = "Category, Product va rasmlar uchun mock data yaratadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Avval mavjud Category va Product larni o‘chiradi',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted = Product.objects.count(), Category.objects.count()
            Category.objects.all().delete()  # CASCADE productlarni ham o'chiradi
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f'O‘chirildi: {deleted[0]} product, {deleted[1]} category'
            ))

        created_products = 0
        for title, data in CATEGORIES.items():
            category, _ = Category.objects.get_or_create(title=title)

            for name, price, description in data['products']:
                if Product.objects.filter(name=name).exists():
                    continue

                product = Product.objects.create(
                    name=name,
                    description=description,
                    price=Decimal(price),
                    stock=random.randint(0, 40),
                    discount=random.choice([0, 0, 0, 5, 10, 15, 20, 30]),
                    category=category,
                )
                filename = name.lower().replace(' ', '_').replace('"', '') + '.jpg'
                product.image.save(
                    filename,
                    ContentFile(make_image(name, title, data['color'])),
                    save=True,
                )
                created_products += 1

            self.stdout.write(f'  {title}: {category.products.count()} ta mahsulot')

        self.stdout.write(self.style.SUCCESS(
            f'\nTayyor — {created_products} ta yangi mahsulot qo‘shildi. '
            f'Jami: {Category.objects.count()} category, {Product.objects.count()} product.'
        ))
