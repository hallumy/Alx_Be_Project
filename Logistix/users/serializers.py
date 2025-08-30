
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role',
            'first_name', 'last_name', 'address',
            'date_of_birth', 'profile_pic'
        ]
        read_only_fields = ['id']

