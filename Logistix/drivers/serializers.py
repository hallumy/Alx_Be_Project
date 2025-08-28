
from rest_framework import serializers
from .models import Driver
from django.contrib.auth import get_user_model

User = get_user_model()
 
class DriverSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='driver').exclude(id__in=Driver.objects.values_list('user_id', flat=True))
    )

    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

