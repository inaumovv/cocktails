# Generated by Django 4.2.3 on 2024-08-14 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_remove_recipe_ingredients_alter_recipe_instruction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='recipes/'),
        ),
    ]
