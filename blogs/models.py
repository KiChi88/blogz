from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from . task import send_email

# Личный блог и список читаемых блогов
class Blogs(models.Model):
    user  = models.OneToOneField(User, on_delete = models.CASCADE, related_name='user', verbose_name='Пользователь')
    blogs = models.ManyToManyField(User, null=True, blank=True, related_name='blogs', verbose_name='Читает')

    class Meta:
        verbose_name = 'Блог пользователя'
        verbose_name_plural = 'Блоги пользователей'

    def __str__(self):
        return self.user.username

# Блог создается автоматически после создания пользователя
@receiver(post_save, sender=User)
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        Blogs.objects.create(user=instance)

# Посты
class Posts(models.Model):
    user  = models.ForeignKey(User, null=True, on_delete = models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=250, null=True, verbose_name='Заголовок')
    text  = models.TextField(null=True, verbose_name='Текст')
    date  = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('blogs:post', args=[str(self.id)])

    def __str__(self):
        return self.user.username + ': ' + self.title[:50] + \
            '...' if len(self.title[:50]) > 50 else self.user.username + ': ' + self.title

# Статус прочтения поста
class Status(models.Model):
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Posts, null=True, on_delete = models.CASCADE, verbose_name='Пост')
    read = models.BooleanField(default=False, verbose_name = 'Прочитан')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Статус прочтения поста'
        verbose_name_plural = 'Статус прочтения поста'

    def __str__(self):
        return self.user.username + ': ' + self.post.title[:50] + \
            '...' if len(self.post.title[:50]) > 50 else self.user.username + ': ' + self.post.title

# После создания поста автоматически создаются все необходимые статусы и отправляются уведомления на почту
@receiver(post_save, sender=Posts)
def new_post(sender, instance, created, **kwargs):
    if created:
        url   = 'http://localhost:8000' + instance.get_absolute_url()
        name  = instance.user.username
        title = instance.title
        persons = [person for person in User.objects.all() if instance.user in person.user.blogs.all()]
        for person in persons:
            Status.objects.create(
                    user = person,
                    post = instance
                )
            send_email.delay(person.id, url, name, title)