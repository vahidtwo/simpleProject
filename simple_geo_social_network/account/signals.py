
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from account.models import User


@receiver(pre_save, sender=User)
def pre_save_location_time(sender, instance, *args, **kwargs):
    if instance.email:
        try:
            old_instance = User.objects.get(email=instance.email)
            if old_instance.lat != instance.lat or old_instance.lng != instance.lng:
                instance.location_time = timezone.now()
            pre_save.disconnect(pre_save_location_time, sender=User)
            instance.save()
            pre_save.connect(pre_save_location_time, sender=User)
        except User.DoesNotExist:
            pass
