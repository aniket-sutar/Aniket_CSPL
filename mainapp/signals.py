from django.db.models.signals import post_save
from .models import Department,Employee,PlaceOrder
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save,sender=Department)
def deactivate_employees(sender ,instance ,**kwargs):
    if not instance.is_active:
        instance.employees.update(is_active=False)
    else:
        instance.employees.update(is_active=True)

@receiver(post_save,sender=PlaceOrder)
def send_message_channel(sender,instance,created ,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
                    "notifications",
                    {
                        "type": "send_notification",
                        "message": f"Hurrah!....Your order placed successfully!",
                    }
                )