# Generated by Django 3.2.8 on 2021-11-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_shopuserprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuserprofile',
            name='about_me',
            field=models.TextField(blank=True, max_length=512, verbose_name='Обо мне'),
        ),
    ]