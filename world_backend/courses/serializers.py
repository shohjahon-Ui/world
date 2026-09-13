from rest_framework import serializers

from .models import Course, Level, Lesson


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'lesson_type', 'is_locked', 'video_url']

    def get_video_url(self, obj):
        request = self.context.get('request')
        if obj.video_file and request:
            return request.build_absolute_uri(obj.video_file.url)
        return None


class LevelSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Level
        fields = ['id', 'name', 'order', 'lessons']


class CourseListSerializer(serializers.ModelSerializer):
    """Kurslar ro'yxati uchun — qisqa ma'lumot (dashboard kartalari uchun)."""

    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'icon_emoji', 'description']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Bitta kurs ichidagi barcha darajalar va darslar (course-path sahifasi uchun)."""

    levels = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'icon_emoji', 'description', 'levels']
