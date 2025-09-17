from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        from django.contrib.auth.models import Group
        group_map = {
            'doctor': 'Doctors',
            'medsestra': 'Medsestras',
            'patient': 'Patients'
        }
        if instance.role in group_map:
            group, _ = Group.objects.get_or_create(name=group_map[instance.role])
            instance.groups.add(group)
