# Generated by Django 2.0.7 on 2018-12-13 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20181213_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['-id'], 'verbose_name': 'Статус прочтения поста', 'verbose_name_plural': 'Статус прочтения поста'},
        ),
    ]