import profile
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

from .models import Profile
from .views import generate_otp


def send_otp_mail(recipient,code):
    subject = 'welcome to Excel_Comp '
    message = f'Hi {recipient.username}, thank you for registering in Excel_Comp. Kindly use the below code to verify your account \n{code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient.email, ]
    send_mail( subject, message, email_from, recipient_list )

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_otp = generate_otp()
        profile = Profile.objects.create(user=instance,otp=user_otp)
        profile.save()

        # send mail containing otp to user
        send_otp_mail(instance,user_otp)
        
        