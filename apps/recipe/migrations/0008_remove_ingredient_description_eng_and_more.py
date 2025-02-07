# Generated by Django 4.2.3 on 2024-09-19 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_ingredient_description_eng_ingredient_name_eng_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='description_eng',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='name_eng',
        ),
        migrations.RemoveField(
            model_name='ingredientcategory',
            name='name_eng',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='description_eng',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='history_eng',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='how_to_use_eng',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='name_eng',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='language',
            field=models.CharField(choices=[('ENG', 'Английский'), ('RUS', 'Русский')], default='RUS', max_length=20, verbose_name='Язык'),
        ),
        migrations.AddField(
            model_name='ingredientcategory',
            name='language',
            field=models.CharField(choices=[('ENG', 'Английский'), ('RUS', 'Русский')], default='RUS', max_length=20, verbose_name='Язык'),
        ),
        migrations.AddField(
            model_name='tool',
            name='language',
            field=models.CharField(choices=[('ENG', 'Английский'), ('RUS', 'Русский')], default='RUS', max_length=20, verbose_name='Язык'),
        ),
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='recipe_ingr_name_0ead22_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['title'], name='recipe_reci_title_4b9b8b_idx'),
        ),
    ]
