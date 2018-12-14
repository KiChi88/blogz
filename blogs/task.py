import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from main.celery import app
 
# Отправка почты с помощью Celery
@app.task
def send_email(person_id, url, name, title):
    UserModel = get_user_model()
    try:
        person = UserModel.objects.get(id=person_id)
        send_mail(
            'BlogZ: новый пост',
            'Пользователь ' + name + ' добавил новый пост - \n' + 
            title + '\n' +
            url,
            'django@gmail.com',
            [person.email],
            fail_silently=False,
        )
    except Exception as e:
        logging.warning(e)