@echo off
REM World loyihasini Windows'da bir zumda ishga tushirish

echo === 1. Virtual muhit (venv) yaratilmoqda ===
python -m venv venv

echo === 2. venv faollashtirilmoqda ===
call venv\Scripts\activate.bat

echo === 3. Kerakli paketlar o'rnatilmoqda ===
pip install -r requirements.txt

echo === 4. Ma'lumotlar bazasi migratsiyalari ===
python manage.py migrate

echo === 5. Boshlang'ich kurslar yaratilmoqda (English, Russian, Math, Chinese, Korean) ===
python manage.py seed_courses

echo.
echo Tayyor! Admin foydalanuvchi yaratish uchun quyidagini yozing:
echo     python manage.py createsuperuser
echo Keyin serverni ishga tushiring:
echo     python manage.py runserver
echo.
pause
