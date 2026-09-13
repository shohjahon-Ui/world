from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from courses.views import ai_chat_view, books_view, course_path_view, quiz_view

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('course/<slug:slug>/', course_path_view, name='course-path'),
    path('books/', books_view, name='books'),
    path('ai-chat/', ai_chat_view, name='ai-chat'),
    path('quiz/<int:level_id>/', quiz_view, name='quiz'),
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),
]

# Development rejimida video/rasm fayllarni to'g'ridan-to'g'ri ko'rsatish uchun
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
