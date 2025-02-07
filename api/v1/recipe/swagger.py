from .serializers import *
from api.base.swagger import filter_params

tags = ['recipe']

ingredient_category_block_list = {
    'operation_description': '## Список секция категорий',
    'operation_summary': 'Список секция категорий',
    'responses': {'200': IngredientCategorySectionSerializer()},
    'tags': tags,
}

ingredient_retrieve = {
    'operation_description': '## Страница ингредиента',
    'operation_summary': 'Получение страницы ингредиента',
    'responses': {'200': IngredientSerializer()},
    'tags': tags,
}

ingredient_category_list = {
    'operation_description': '## Список категорий ингредиентов',
    'operation_summary': 'Получение списока категорий ингредиентов',
    'responses': {'200': IngredientCategorySerializer(many=True)},
    'tags': tags,
}

tool_list = {
    'operation_description': '## Список инструментов',
    'operation_summary': 'Получение списока инструментов',
    'responses': {'200': ViewToolSerializer(many=True)},
    'tags': tags,
}

tool_retrieve = {
    'operation_description': '## Страница инструмента',
    'operation_summary': 'Получение страницы инструмента',
    'responses': {'200': ViewToolSerializer()},
    'tags': tags,
}

recipe_selection = {
    'operation_description': '## Поиск рецепта по ингредиентам',
    'operation_summary': 'Поиск рецепта по ингредиентам',
    'request_body': SelectionRecipeSerializer,
    'responses': {'200': SelectionRecipeSerializer(many=True)},
    'tags': tags,
}

recipe_list = {
    'operation_description': '## Список рецепта',
    'operation_summary': 'Получение Списока рецепта',
    'responses': {'200': RecipeListSerializer(many=True)},
    'tags': tags,
    'manual_parameters': filter_params,
}

recipe_update = {
    'operation_description': '## Изменение рецепта',
    'operation_summary': 'Изменение рецепта',
    'request_body': UpdateRecipeSerializer(),
    'responses': {'200': RecipeDetailSerializer()},
    'tags': tags,
}

recipe_delete = {
    'operation_description': '## Удаление рецепта',
    'operation_summary': 'Удаление рецепта',
    'responses': {'200': 'Deleted'},
    'tags': tags,
}

recipe_create = {
    'operation_description': '## Создание рецепта',
    'operation_summary': 'Создание рецепта',
    'request_body': CreateRecipeSerializer(),
    'responses': {'201': RecipeDetailSerializer()},
    'tags': tags,
}

recipe_retrieve = {
    'operation_description': '## Страница рецепта',
    'operation_summary': 'Получение страницы рецепта',
    'responses': {'200': RecipeDetailSerializer()},
    'tags': tags,
}
