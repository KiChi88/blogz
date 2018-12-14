# Generated by Django 2.0.7 on 2018-12-12 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0002_person'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AddField(
            model_name='posts',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='posts',
            name='title',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
