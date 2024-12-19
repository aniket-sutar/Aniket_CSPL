from rest_framework import serializers
from .models import SystemUser, Roles ,Product,Category,Department,Employee

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
    
class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)  
    # prod_name = serializers.CharField(max_length=50)
    # price = serializers.IntegerField()
    # desc = serializers.CharField(read_only=True)

    # desc = serializers.CharField(read_only=True) 
    class Meta:
        model = Product
        fields = ('id','prod_name','price','desc')
        # read_only_fields = ('desc',)

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cat_name = serializers.CharField(max_length=50)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.cat_name = validated_data.get('cat_name', instance.cat_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id','dept_name')
    
class EmployeeSerializer(serializers.ModelSerializer):
    dept_name = serializers.CharField(source='dept_id.dept_name')
    class Meta:
        model = Employee
        fields = ('id','emp_name','emp_age','dept_name')
