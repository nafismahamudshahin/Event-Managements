from django.contrib.auth.models import User , Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from participants.views import mail_send

@receiver(post_save,sender= User)
def activate_mail_send(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FORNTEND_URL}/activate/{instance.id}/{token}/"
        subject = "Activate Your Account"
        message = f"Hi {instance.first_name} {instance.last_name}\nPlease Activate Your account\nLink:{activation_url}"
        recipient_email = [instance.email]
        try:
            mail_send(subject,message,recipient_email)
        except Exception as e:
            print(f"Faild to send Email to {instance.email}: {str(e)}")

@receiver(post_save,sender=User)
def assigned_role(sender,instance,created,**kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()