from rest_framework import serializers
from .models import SystemUser, Roles

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'name', 'is_active']

class SystemUserSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all())

    class Meta:
        model = SystemUser
        fields = ['id', 'username', 'email', 'mobile_no', 'profile_image', 'role_id', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = SystemUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            mobile_no=validated_data.get('mobile_no'),
            profile_image=validated_data.get('profile_image'),
            role_id=validated_data.get('role_id')
        )
        return user