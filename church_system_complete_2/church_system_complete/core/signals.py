from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Student  

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and not (instance.is_superuser or instance.is_staff):
        Student.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )