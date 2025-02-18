from rest_framework import serializers

from apps.user.models import Referral, User


class AdminReferralSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_user(self, value):
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')
        return value

    class Meta:
        model = Referral
        fields = ['id', 'code', 'code_applying', 'user']
        read_only_fields = ['code_applying']
