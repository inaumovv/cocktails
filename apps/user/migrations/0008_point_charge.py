# Generated by Django 4.2.3 on 2024-09-25 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_point_created_at_point_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='charge',
            field=models.BooleanField(default=False, verbose_name='Списание?'),
        ),
    ]
