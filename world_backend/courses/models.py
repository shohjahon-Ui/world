from django.db import models


class Course(models.Model):
    """Til yoki fan kursi — masalan: Ingliz tili, Matematika."""

    name = models.CharField('Nomi', max_length=100)
    slug = models.SlugField('Slug', unique=True, help_text="Masalan: english, russian, math, chinese, korean")
    icon_emoji = models.CharField('Belgi (emoji)', max_length=10, blank=True, default='📘')
    description = models.TextField('Tavsif', blank=True)
    order = models.PositiveIntegerField('Tartib', default=0)
    is_active = models.BooleanField('Faol', default=True)

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Level(models.Model):
    """Kurs ichidagi daraja — masalan: Elementary, Pre-Intermediate."""

    course = models.ForeignKey(Course, related_name='levels', on_delete=models.CASCADE, verbose_name='Kurs')
    name = models.CharField('Nomi', max_length=100)
    order = models.PositiveIntegerField('Tartib', default=0)

    class Meta:
        verbose_name = 'Daraja'
        verbose_name_plural = 'Darajalar'
        ordering = ['order']

    def __str__(self):
        return f'{self.course.name} — {self.name}'


def lesson_video_path(instance, filename):
    """Videolarni har bir kurs uchun alohida papkaga joylashtiradi:
    media/courses/<course-slug>/videos/<fayl-nomi>
    """
    course_slug = instance.level.course.slug
    return f'courses/{course_slug}/videos/{filename}'


class Lesson(models.Model):
    """Bitta video dars."""

    LESSON_TYPES = [
        ('video', "O'rganish (video)"),
        ('practice', 'Amaliyot'),
        ('mixed', "O'rganish va amaliyot"),
    ]

    level = models.ForeignKey(Level, related_name='lessons', on_delete=models.CASCADE, verbose_name='Daraja')
    title = models.CharField('Sarlavha', max_length=200)
    order = models.PositiveIntegerField('Tartib', default=0)
    lesson_type = models.CharField('Turi', max_length=20, choices=LESSON_TYPES, default='video')

    # Video fayl — hozircha bo'sh, keyinroq o'zingiz admin panel orqali yuklaysiz
    video_file = models.FileField('Video fayl', upload_to=lesson_video_path, blank=True, null=True)

    is_locked = models.BooleanField('Qulflangan', default=True)

    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'
        ordering = ['order']

    def __str__(self):
        return f'{self.level} — {self.order}. {self.title}'


def book_cover_path(instance, filename):
    """Kitob muqovalarini har bir kurs uchun alohida papkaga joylashtiradi."""
    course_slug = instance.course.slug
    return f'courses/{course_slug}/books/{filename}'


class Book(models.Model):
    """Onlayn kitob — bitta fan/til kursiga bog'langan."""

    course = models.ForeignKey(Course, related_name='books', on_delete=models.CASCADE, verbose_name='Fan/til')
    title = models.CharField('Sarlavha', max_length=200)
    price_usd = models.DecimalField('Narxi (USD)', max_digits=6, decimal_places=2, default=15)
    cover_image = models.ImageField('Muqova', upload_to=book_cover_path, blank=True, null=True)
    pdf_file = models.FileField('Kitob fayli (PDF)', upload_to=book_cover_path, blank=True, null=True)
    is_available = models.BooleanField("Sotuvda", default=True)
    order = models.PositiveIntegerField('Tartib', default=0)

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'
        ordering = ['order', 'title']

    def __str__(self):
        return f'{self.title} ({self.course.name})'


class Quiz(models.Model):
    """Bitta daraja (Level) uchun test — bir nechta savoldan iborat."""

    level = models.OneToOneField(Level, related_name='quiz', on_delete=models.CASCADE, verbose_name='Daraja')
    title = models.CharField('Sarlavha', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'

    def __str__(self):
        return self.title or f'{self.level} — test'


class Question(models.Model):
    """Test ichidagi bitta savol."""

    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, verbose_name='Test')
    text = models.CharField('Savol matni', max_length=300)
    order = models.PositiveIntegerField('Tartib', default=0)

    class Meta:
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'
        ordering = ['order']

    def __str__(self):
        return self.text


class Choice(models.Model):
    """Savol ichidagi bitta javob varianti."""

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, verbose_name='Savol')
    text = models.CharField('Javob matni', max_length=200)
    is_correct = models.BooleanField("To'g'ri javobmi", default=False)

    class Meta:
        verbose_name = 'Javob varianti'
        verbose_name_plural = 'Javob variantlari'

    def __str__(self):
        return self.text
