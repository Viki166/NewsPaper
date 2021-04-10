from .models import *
from django.db.models.signals import post_save, post_delete
from django.core.mail import mail_managers
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .views import Mailing


# @receiver(post_save, sender=Appointment)  # получатель
# def notify_managers_appointment(sender, instance, created, **kwargs): # модель(отправитель), сущность,которая создается или сохраняется, создана ли эта сущность в БД
#     msg = EmailMultiAlternatives(
#         subject=f'{instance.client_name} {instance.date.strftime("%d %m %Y")}',
#         body=instance.message,
#         from_email='bobby.loner27@gmail.com',
#         to=['viki49661@gmail.com'],
#     )
#     msg.send()




