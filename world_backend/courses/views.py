from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Course, Level
from .serializers import CourseDetailSerializer, CourseListSerializer


class CourseListView(ListAPIView):
    """GET /api/courses/  — barcha kurslar ro'yxati (dashboard uchun)."""
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseListSerializer


class CourseDetailView(RetrieveAPIView):
    """GET /api/courses/<slug>/  — bitta kursning darajalari va darslari."""
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'


def course_path_view(request, slug):
    """Oddiy sahifa: /course/<slug>/ — kurs ichidagi darajalar va darslar yo'li."""
    course = get_object_or_404(
        Course.objects.prefetch_related('levels__lessons'),
        slug=slug,
        is_active=True,
    )
    levels = list(course.levels.all())
    # Birinchi bo'sh bo'lmagan yoki shunchaki birinchi darajani "faol" qilib ko'rsatamiz
    active_level = levels[0] if levels else None
    return render(request, 'course_path.html', {
        'course': course,
        'levels': levels,
        'active_level': active_level,
    })


def books_view(request):
    """Sahifa: /books/ — barcha fanlar bo'yicha onlayn kitoblar do'koni."""
    courses = Course.objects.filter(is_active=True).prefetch_related('books')
    return render(request, 'books.html', {'courses': courses})


def ai_chat_view(request):
    """Sahifa: /ai-chat/ — World AI bilan suhbat."""
    return render(request, 'ai_chat.html')


def quiz_view(request, level_id):
    """Sahifa: /quiz/<level_id>/ — bitta darajaning testi."""
    level = get_object_or_404(Level.objects.select_related('course'), id=level_id)
    quiz = getattr(level, 'quiz', None)
    questions = quiz.questions.prefetch_related('choices').all() if quiz else []
    return render(request, 'quiz.html', {'level': level, 'quiz': quiz, 'questions': questions})
