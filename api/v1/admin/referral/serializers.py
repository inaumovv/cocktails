from rest_framework import serializers

from apps.user.models import Referral, User


class AdminReferralSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    def validate_user(self, value):
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')
        return value

    class Meta:
        model = Referral
        fields = ['id', 'user', 'code', 'code_applying']


class AdminUserReferralSerializer(serializers.ModelSerializer):
    ref_code = AdminReferralSerializer(read_only=True, many=False)

    class Meta:
        model = User
        fields = ('id', 'ref_code')
