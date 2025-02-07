# Generated by Django 4.2.3 on 2024-09-19 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_recipe_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='description_eng',
            field=models.CharField(blank=True, null=True, verbose_name='Описание на английском'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='name_eng',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название на английском'),
        ),
        migrations.AddField(
            model_name='ingredientcategory',
            name='name_eng',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название категории на английском'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='language',
            field=models.CharField(choices=[('ENG', 'Английский'), ('RUS', 'Русский')], default='RUS', max_length=20, verbose_name='Язык'),
        ),
        migrations.AddField(
            model_name='tool',
            name='description_eng',
            field=models.CharField(blank=True, null=True, verbose_name='Описание на английском'),
        ),
        migrations.AddField(
            model_name='tool',
            name='history_eng',
            field=models.CharField(blank=True, null=True, verbose_name='История на английском'),
        ),
        migrations.AddField(
            model_name='tool',
            name='how_to_use_eng',
            field=models.CharField(blank=True, null=True, verbose_name='Как использовать на английском'),
        ),
        migrations.AddField(
            model_name='tool',
            name='name_eng',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название на английском'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='type',
            field=models.CharField(choices=[('ounce', 'унция'), ('ml', 'мл'), ('gram', 'грамм'), ('piece', 'шт'), ('spoon', 'ложка'), ('cup', 'кружка'), ('tablespoon', 'столовая ложка'), ('teaspoon', 'чайная ложка'), ('slice', 'ломтик'), ('twist', 'твист'), ('cube', 'кубик'), ('sprig', 'веточка'), ('pinch', 'щепотка'), ('spiral', 'спираль'), ('wedge', 'долька'), ('dash', 'дэш'), ('block', 'блок'), ('circle', 'кружок')], default='ounce', max_length=30, verbose_name='Мера'),
        ),
    ]
