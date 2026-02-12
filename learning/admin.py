from django.contrib import admin
from .models import Topic, Progress

    
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "is_completed", "completed_at")

