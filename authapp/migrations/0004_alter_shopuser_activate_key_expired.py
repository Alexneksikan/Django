# Generated by Django 3.2.8 on 2021-11-20 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_alter_shopuser_activate_key_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activate_key_expired',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]