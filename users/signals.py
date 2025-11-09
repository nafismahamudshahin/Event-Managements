from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from core.views import send_mail_to_user
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save,sender= User)
def activate_mail_send(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FORNTEND_URL}/activate/{instance.id}/{token}/"
        subject = "Activate Your Account"
        message = f"Hi {instance.first_name} {instance.last_name}\nPlease Activate Your account\nLink:{activation_url}"
        recipient_email = [instance.email]
        try:
            send_mail_to_user(subject,message,recipient_email)
        except Exception as e:
            print(f"Faild to send Email to {instance.email}: {str(e)}")

@receiver(post_save,sender=User)
def assigned_role(sender,instance,created,**kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()