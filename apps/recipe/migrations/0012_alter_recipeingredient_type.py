# Generated by Django 4.2.3 on 2024-10-23 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_ingredientcategorysection_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='type',
            field=models.CharField(choices=[('ounce', 'унция'), ('ml', 'мл'), ('gram', 'грамм'), ('piece', 'шт'), ('spoon', 'ложка'), ('cup', 'кружка'), ('tablespoon', 'столовая ложка'), ('teaspoon', 'чайная ложка'), ('slice', 'ломтик'), ('twist', 'твист'), ('cube', 'кубик'), ('sprig', 'веточка'), ('pinch', 'щепотка'), ('spiral', 'спираль'), ('wedge', 'долька'), ('dash', 'дэш'), ('block', 'блок'), ('circle', 'кружок'), ('bottle', 'бутылка')], default='ounce', max_length=30, verbose_name='Мера'),
        ),
    ]
