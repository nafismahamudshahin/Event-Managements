from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

@receiver(post_save,sender= User)
def activate_mail_send(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FORNTEND_URL}/activate/{instance.id}/{token}/"
        subject = "Activate Your Account"
        form_email = "nafismahamudshahin@gmail.com"
        message = f"Hi {instance.first_name} {instance.last_name}\nPlease Activate Your account\nLink:{activation_url}"
        recipient_email = [instance.email]
        try:
            send_mail(subject,message,form_email,recipient_email)
        except Exception as e:
            print(f"Faild to send Email to {instance.email}: {str(e)}")
