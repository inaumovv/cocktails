from rest_framework import serializers
from apps.user.models import *
from apps.recipe.models import *
from django.db.models import Sum
from api.v1.recipe.serializers import RecipeDetailSerializer
from django.contrib.auth.hashers import make_password


__all__ = [
    'AdminUserRecipeSerializer',
    'AdminPointSerializer',
    'AdminReferralSerializer',
    'AdminUserSerializer',
    'AdminFavoriteRecipeSerializer',
    'AdminUserListSerializer',
    'AdminUserUpdateSerializer',
    'AdminUserCreateSerializer',
]


class AdminUserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class AdminPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['points']


class AdminReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


class AdminFavoriteRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeDetailSerializer()

    class Meta:
        model = FavoriteRecipe
        fields = ['recipe']


class AdminUserSerializer(serializers.ModelSerializer):
    points = AdminPointSerializer(many=True, read_only=True)
    points_total = serializers.SerializerMethodField()
    referral = AdminReferralSerializer(many=True, read_only=True)
    recipes = AdminUserRecipeSerializer(many=True, read_only=True)
    favorite = AdminFavoriteRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_points_total(self, obj):
        total_points = obj.points.filter(charge=False).aggregate(total_points=Sum('points'))['total_points'] or 0
        charged_points = obj.points.filter(charge=True).aggregate(total_charged=Sum('points'))['total_charged'] or 0
        return total_points - charged_points


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    avatar = serializers.FileField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(write_only=True, required=False)
    is_active = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'is_staff',
                  'date_of_birth',
                  'password',
                  'first_name',
                  'last_name',
                  'is_active',
                  'gender',
                  'phone',
                  'avatar'
                  ]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'phone', 'first_name', 'last_name', 'gender',
            'date_of_birth', 'avatar', 'is_active', 'is_staff', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user