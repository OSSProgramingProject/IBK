from django.contrib import admin
from .models import UserProfile
from .models import Problem

admin.site.register(UserProfile)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'difficulty')
    search_fields = ('title', 'tags')