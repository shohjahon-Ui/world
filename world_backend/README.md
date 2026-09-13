# World — Backend (Django)

Bu loyiha "World" platformasining orqa qismi (backend). 5 ta kurs uchun
tayyor papka strukturasi bor: **Ingliz, Rus, Matematika, Xitoy, Koreys**.
Video darslarni keyinroq o'zingiz admin panel orqali yuklaysiz.

## 1-usul: Avtomatik o'rnatish (tavsiya etiladi)

**Windows:**
```
setup.bat
```
(fayl ustiga ikki marta bosing yoki terminalda yozing)

**Linux / macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

Bu skript avtomatik ravishda: venv yaratadi → faollashtiradi → paketlarni
o'rnatadi → bazani tayyorlaydi → 5 ta kursni yaratadi.

## 2-usul: Qo'lda o'rnatish (qadam-baqadam)

```bash
# 1. Virtual muhit yaratish
python -m venv venv

# 2. Faollashtirish
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

# 3. Paketlarni o'rnatish
pip install -r requirements.txt

# 4. Ma'lumotlar bazasini tayyorlash
python manage.py migrate

# 5. 5 ta boshlang'ich kursni yaratish (bo'sh, darslarsiz)
python manage.py seed_courses

# 6. Admin foydalanuvchi yaratish (o'zingiz uchun login/parol)
python manage.py createsuperuser

# 7. Serverni ishga tushirish
python manage.py runserver
```

Server ishga tushgach: **http://127.0.0.1:8000/admin/** manziliga kiring
(6-qadamda yaratgan login/parol bilan).

## Video darslarni qanday qo'shish kerak?

1. `/admin/` panelga kiring
2. **Courses → Kurslar** bo'limidan kerakli kursni oching (masalan, Ingliz tili)
3. Kerakli darajani (masalan, Elementary) oching
4. Pastda **Lessons** bo'limiga yangi dars qo'shing:
   - Sarlavha (masalan: "Present Simple")
   - Turi (video / amaliyot / aralash)
   - Video fayl — kompyuteringizdan video faylni tanlang
   - Qulflangan — belgini olib tashlasangiz, dars ochiq bo'ladi
5. Saqlang — video avtomatik ravishda quyidagi papkaga tushadi:
   ```
   media/courses/<kurs-nomi>/videos/
   ```

## Papka strukturasi

```
world_backend/
├── manage.py
├── requirements.txt
├── setup.bat / setup.sh
├── config/              → asosiy sozlamalar (settings, urls)
├── courses/             → kurslar ilovasi (models, admin, API)
└── media/courses/
    ├── english/videos/  ← bo'sh, video shu yerga tushadi
    ├── russian/videos/
    ├── math/videos/
    ├── chinese/videos/
    └── korean/videos/
```

## Tayyor API manzillari

- `GET /api/courses/` — barcha kurslar ro'yxati
- `GET /api/courses/english/` — bitta kursning barcha darajalari va darslari

Bu API'ni oldin tayyorlagan dashboard/course-path HTML sahifalariga
ulash uchun ishlatishingiz mumkin.

## Keyingi qadamlar

- Har bir kurs uchun darslarni admin panel orqali qo'shib boring
- Kerak bo'lsa, yangi kurs qo'shish uchun admin panelda **Courses → Add course**
- Productionga chiqarishdan oldin `config/settings.py` ichidagi
  `SECRET_KEY` va `DEBUG = True` qatorlarini albatta o'zgartiring
