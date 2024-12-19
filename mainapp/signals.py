from django.db.models.signals import post_save
from .models import Department,Employee
from django.dispatch import receiver

@receiver(post_save,sender=Department)
def deactivate_employees(sender ,instance ,**kwargs):
    if not instance.is_active:
        instance.employees.update(is_active=False)
    else:
        instance.employees.update(is_active=True)