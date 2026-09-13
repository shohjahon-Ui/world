#!/usr/bin/env bash
# World loyihasini Linux/macOS'da bir zumda ishga tushirish
set -e

echo "=== 1. Virtual muhit (venv) yaratilmoqda ==="
python3 -m venv venv

echo "=== 2. venv faollashtirilmoqda ==="
source venv/bin/activate

echo "=== 3. Kerakli paketlar o'rnatilmoqda ==="
pip install -r requirements.txt

echo "=== 4. Ma'lumotlar bazasi migratsiyalari ==="
python manage.py migrate

echo "=== 5. Boshlang'ich kurslar yaratilmoqda (English, Russian, Math, Chinese, Korean) ==="
python manage.py seed_courses

echo ""
echo "Tayyor! Admin foydalanuvchi yaratish uchun:"
echo "    python manage.py createsuperuser"
echo "Keyin serverni ishga tushiring:"
echo "    python manage.py runserver"
