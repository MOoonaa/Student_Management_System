from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)  # اسم الطالب
    email = models.EmailField(max_length=254, blank=True, null=True, unique=True)
    grade = models.CharField(max_length=50)  # السنة الدراسية (إعدادي/ثانوي...)
    absences = models.IntegerField(default=0)  # مرات الغياب
    score = models.FloatField(default=0.0)  # الدرجات

    def __str__(self):
        return self.name