from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'absences', 'score')
    search_fields = ('name', 'grade')



    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'الاسم الكامل'

    def birth_date(self, obj):
        return obj.dob
    birth_date.short_description = 'تاريخ الميلاد'

    def absence_count(self, obj):
        return obj.absence_count
    absence_count.short_description = 'عدد الغيابات'
