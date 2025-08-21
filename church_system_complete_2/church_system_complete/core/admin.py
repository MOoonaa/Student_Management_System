from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'absences', 'score')
    search_fields = ('name', 'grade')

