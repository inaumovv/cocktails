# Generated by Django 4.2.3 on 2024-08-16 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='links',
            field=models.TextField(null=True, blank=True, verbose_name='Ссылки'),
        ),
    ]
