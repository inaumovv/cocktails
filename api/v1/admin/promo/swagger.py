from api.v1.admin.promo.serializers import AdminPurchasedPromoSerializer

tags = ['admin']

purchased_promo_get = {
    'operation_description': '## Список покупок промокода',
    'operation_summary': 'Получение списка покупок промокода',
    'responses': {'200': AdminPurchasedPromoSerializer(many=True)},
    'tags': tags,
}

purchased_promo_post = {
    'operation_description': '## Создание купленного промокода',
    'operation_summary': 'Создание купленного промокода',
    'request_body': AdminPurchasedPromoSerializer(),
    'responses': {'201': AdminPurchasedPromoSerializer()},
    'tags': tags,
}


