from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from datetime import datetime
import pytz # устраняет разницу объектов типа datetime по UTC, чтобы можно было сравнивать и т.д.
from django.core.mail import mail_managers
from django.db.models.signals import post_save
from .models import *
import time


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
# нужно использовать вместо post_save m2m_changed т.к. нужно получить данные по связи manytomany.
@receiver(m2m_changed, sender=PostCategory)
def signal_post_add(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all() #хотя указали промежуточную модель PostCategory
                                             # в instance будет созданный объект модели Post
        subscribers_emails =[]
        for category in categories:
            subscribers_emails += list(category.subscribers.values_list('email', flat=True))
        subscribers_emails = set(subscribers_emails) # оставили подписчиков в 1 экземпляре,
                                                     # избавились от повторений при подписке на несколько категорий
        for user_email in subscribers_emails:
            text_content = (f'Новая статья в твоем любимом разделе\n'
                            f'{instance.title}\n{instance.content[:50]}\n'
                            f'http://127.0.0.1:8000/news/{instance.id}/')
            html_content = render_to_string('account/email/new_post.html',
                                            {'post': instance, 'user': user_email})
            email = EmailMultiAlternatives(subject=instance.title,
                                           body=text_content,
                                           to=(user_email,))
            email.attach_alternative(html_content, 'text/html')
            email.send()











