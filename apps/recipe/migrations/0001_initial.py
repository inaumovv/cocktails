# Generated by Django 4.2.3 on 2024-07-11 10:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Изменено')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('is_alcoholic', models.BooleanField(default=False, verbose_name='Алкогольный?')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Изменено')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория ингредиента',
                'verbose_name_plural': 'Категории ингредиентов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Изменено')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('history', models.TextField(blank=True, null=True, verbose_name='История')),
                ('how_to_use', models.TextField(blank=True, null=True, verbose_name='Как использовать')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='tool_photos/', verbose_name='Фото')),
                ('links', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None, verbose_name='Ссылки')),
            ],
            options={
                'verbose_name': 'Инструмент',
                'verbose_name_plural': 'Инструменты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('instruction', models.TextField(blank=True, null=True, verbose_name='Инструкция')),
                ('isEnabled', models.BooleanField(default=False, verbose_name='Доступен?')),
                ('moderation_status', models.CharField(choices=[('Draft', 'Черновик'), ('Pending', 'На модерации'), ('Approved', 'Одобрено'), ('Rejected', 'Отклонено'), ('Archive', 'Архив')], default='Draft', max_length=10, verbose_name='Статус модерации')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')),
                ('ingredients', models.ManyToManyField(related_name='recipes_ingr', to='recipe.ingredient', verbose_name='Ингредиенты')),
                ('tools', models.ManyToManyField(related_name='recipes_tool', to='recipe.tool', verbose_name='Инструменты')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['id'],
            },
        ),
    ]
