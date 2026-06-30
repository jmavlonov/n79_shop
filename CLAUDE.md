# Online Shop — Django E-Commerce Project

## Tech Stack

- **Framework**: Django 6.0.6
- **Python**: 3.12
- **Database**: SQLite (`db.sqlite3`)
- **Image Processing**: Pillow 12.2.0
- **Frontend**: Bootstrap 5.2.3 (Start Bootstrap Shop Homepage template)
- **Media Storage**: Local filesystem (`media/`)

## Project Structure

```
online_shop/
├── config/              # Django project configuration
│   ├── settings.py
│   ├── urls.py          # Root URLs: admin/, shop/
│   ├── wsgi.py
│   └── asgi.py
├── app/                 # Main application
│   ├── models.py        # Category, Product, Comment
│   ├── views.py         # home(), product_detail()
│   ├── urls.py          # App-level URL patterns
│   ├── admin.py         # All 3 models registered
│   ├── forms.py         # Empty — not yet implemented
│   ├── utils.py         # product_image_path()
│   ├── migrations/      # 4 migrations
│   ├── templates/app/   # home.html, detail.html
│   └── static/app/      # CSS, JS, images, favicon
├── media/
│   ├── products/        # Organized by category title
│   └── comments/        # Comment file attachments
├── requirements.txt
└── .gitignore
```

## Running the Project

```bash
# Virtual environment activate
source venv/bin/activate

# Migrations
python manage.py migrate

# Development server
python manage.py runserver

# URL: http://127.0.0.1:8000/shop/home/
```

## URL Patterns

| URL | View | Name |
|-----|------|------|
| `/admin/` | Django Admin | — |
| `/shop/home/` | `home()` | `home` |
| `/shop/category/<int:category_id>/products/` | `home()` | `products_of_category` |
| `/shop/detail/<int:pk>` | `product_detail()` | `detail` |

## Models

### Category
```python
title         # CharField, unique=True
created_at    # DateTimeField, auto_now_add
updated_at    # DateTimeField, auto_now
# Reverse: .products (FK from Product)
```

### Product
```python
name          # CharField
description   # TextField, nullable
price         # DecimalField(14, 2)
stock         # PositiveIntegerField, default=0
image         # ImageField → products/<category>/<filename>
category      # ForeignKey(Category, CASCADE)
discount      # PositiveIntegerField, default=0  (percentage)
created_at    # DateTimeField, auto_now_add
updated_at    # DateTimeField, auto_now

# Properties:
# .discounted_price  → price after discount
# .get_image_path    → image URL or fallback placeholder
```

### Comment
```python
name          # CharField(150), nullable
email         # EmailField
message       # TextField
file          # FileField → comments/, nullable
rating        # IntegerField, choices 1–5 (RatingChoices), default=1
product       # ForeignKey(Product, CASCADE, related_name='comments')
created_at    # DateTimeField, auto_now_add
```

## Utility Functions

**`app/utils.py`** — `product_image_path(instance, filename)`
- Upload path: `products/<category_title_lowercase>/<filename>`
- Example: `products/smartfonlar/iphone.jpg`

## Key Settings

```python
DEBUG = True
STATIC_URL = 'assets/'
STATICFILES_DIRS = [BASE_DIR / 'app/static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

> **Muhim**: `SECRET_KEY` development uchun insecure key — productonga chiqishdan oldin o'zgartirish shart.

## Implemented vs Incomplete Features

### Ishlaydi
- Mahsulotlarni kategoriya bo'yicha filtrlash
- Mahsulot detail sahifasi
- Commentlarni ko'rish (faqat o'qish)
- Chegirma hisoblash (property orqali)
- Admin panel (Category, Product, Comment)
- Media fayl yuklash va saqlash

### Tugallanmagan
- Comment qo'shish formi (HTML bor, backend yo'q)
- Buyurtma berish formi (HTML bor, backend yo'q)
- Sort/Filter tugmalari — Expensive, Cheap, Likes (UI bor, logic yo'q)
- `forms.py` — bo'sh fayl
- Related products (detail.html'da hardcoded dummy ma'lumotlar)

## Migration History

1. `0001_initial` — `Catogory` model (eski noto'g'ri nom)
2. `0002_rename` — `Catogory` → `Category` (to'g'rilandi)
3. `0003_alter` — Timestamplar va Meta options qo'shildi
4. `0004_alter_product_image_comment` — Product va Comment modellari

## Development Notes

- Loyiha aktiv ishlanish bosqichida
- Frontend formlar mavjud lekin backend bilan bog'lanmagan
- `db.sqlite3` va `media/` `.gitignore`da — commitlanmaydi
- `venv/` git keshidan olib tashlandi (`git rm --cached`)
