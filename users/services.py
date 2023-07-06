from django.core.mail import send_mail

from config import settings


def send_email_activate(email, pk):
    send_mail(
        'Активация профиля',
        f'Добрый день.\nДля активации профиля на сайте перейдите по ссылке http://127.0.0.1:8000/users/confirm_email/{pk}',
        settings.EMAIL_HOST_USER,
        email
    )