from django.core.management.base import BaseCommand

from courses.models import Course, Level

COURSES = [
    {
        'name': 'Ingliz tili',
        'slug': 'english',
        'icon_emoji': '🇬🇧',
        'levels': ['Elementary', 'Pre-Intermediate', 'Intermediate', 'Upper-Intermediate'],
    },
    {
        'name': 'Rus tili',
        'slug': 'russian',
        'icon_emoji': '🇷🇺',
        'levels': ['Elementary', 'Pre-Intermediate', 'Intermediate', 'Upper-Intermediate'],
    },
    {
        'name': 'Matematika',
        'slug': 'math',
        'icon_emoji': '➗',
        'levels': ['Boshlang\'ich', "O'rta", "Ilg'or"],
    },
    {
        'name': 'Xitoy tili',
        'slug': 'chinese',
        'icon_emoji': '🇨🇳',
        'levels': ['HSK 1', 'HSK 2', 'HSK 3'],
    },
    {
        'name': 'Koreys tili',
        'slug': 'korean',
        'icon_emoji': '🇰🇷',
        'levels': ['TOPIK boshlang\'ich', 'TOPIK o\'rta'],
    },
]


class Command(BaseCommand):
    help = "5 ta boshlang'ich kurs va ularning darajalarini yaratadi (darslarsiz, bo'sh holatda)."

    def handle(self, *args, **options):
        for i, course_data in enumerate(COURSES):
            course, created = Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults={
                    'name': course_data['name'],
                    'icon_emoji': course_data['icon_emoji'],
                    'order': i,
                },
            )
            status = 'yaratildi' if created else 'allaqachon mavjud'
            self.stdout.write(self.style.SUCCESS(f"Kurs '{course.name}' — {status}"))

            for j, level_name in enumerate(course_data['levels']):
                level, level_created = Level.objects.get_or_create(
                    course=course,
                    name=level_name,
                    defaults={'order': j},
                )
                if level_created:
                    self.stdout.write(f"  + daraja qo'shildi: {level_name}")

        self.stdout.write(self.style.SUCCESS(
            "\nTayyor! Endi admin panelga kiring va har bir daraja ichiga darslarni "
            "(sarlavha + video fayl) qo'shishingiz mumkin."
        ))
