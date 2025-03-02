from django.db import transaction
from rest_framework import serializers

from apps.recipe.models import Tool, Recipe, RecipeIngredient, Ingredient


class AdminRecipeToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class AdminRecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'name', 'quantity', 'type']

    def get_name(self, obj):
        return obj.ingredient.name


class AdminListRecipeSerializer(serializers.ModelSerializer):
    tools = AdminRecipeToolSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()

    def get_favorites_count(self, obj: Recipe):
        return obj.favorited_by.count()

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'instruction',
            'isEnabled',
            'photo',
            'user',
            'ingredients',
            'tools',
            'favorites_count',
            'is_alcoholic',
            'language',
            'moderation_status',
            'video_url',
        ]


    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return AdminRecipeIngredientSerializer(recipe_ingredients, many=True).data


class AdminCreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = AdminRecipeIngredientSerializer(source='recipe_ingredients', many=True)
    tools = serializers.PrimaryKeyRelatedField(queryset=Tool.objects.all(), many=True),

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', [])
        tools_data = validated_data.pop('tools', [])

        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)

            for ingredient_data in ingredients_data:
                ingredient = ingredient_data['ingredient']
                if not ingredient:
                    raise serializers.ValidationError(f"Ingredient with id {ingredient} does not exist.")
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=ingredient_data['quantity'],
                    type=ingredient_data['type']
                )

            if tools_data:
                recipe.tools.set(tools_data)

        return recipe

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'instruction',
            'isEnabled',
            'photo',
            'user',
            'ingredients',
            'tools',
            'is_alcoholic',
            'language',
            'moderation_status',
            'video_url',
        ]


class AdminUpdateRecipeSerializer(serializers.ModelSerializer):
    ingredients = AdminRecipeIngredientSerializer(source='recipe_ingredients', many=True)

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'instruction',
            'isEnabled',
            'photo',
            'user',
            'ingredients',
            'tools',
            'is_alcoholic',
            'language',
            'moderation_status',
            'video_url',
        ]

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        instance = super().update(instance, validated_data)

        instance.recipe_ingredients.all().delete()

        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient_id=ingredient_data['ingredient']['id'],
                quantity=ingredient_data['quantity'],
                type=ingredient_data['type']
            )

        return instance
