from django.contrib import admin

from .models import Book, Choice, Course, Level, Lesson, Question, Quiz


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('order', 'title', 'lesson_type', 'video_file', 'is_locked')


class LevelInline(admin.TabularInline):
    model = Level
    extra = 1
    fields = ('order', 'name')


class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ('order', 'title', 'price_usd', 'cover_image', 'pdf_file', 'is_available')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_emoji', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LevelInline, BookInline]


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'lesson_type', 'is_locked', 'video_file')
    list_filter = ('level__course', 'lesson_type', 'is_locked')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'price_usd', 'is_available')
    list_filter = ('course', 'is_available')


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    fields = ('text', 'is_correct')


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ('order', 'text')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'level')
    list_filter = ('level__course',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    inlines = [ChoiceInline]
