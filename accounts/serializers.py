from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'default': True},
            'is_staff': {'default': False},
            'is_superuser': {'default': False} 
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
        
    def validate(self,data):
            username = data.get('username')
            password = data.get('password')
            
            if username and password:
                user = authenticate(username=username,password=password)
                
                if user:
                    if user.is_active:
                        data['user'] = user
                    else:
                        msg = 'User is deactivated'
                        raise serializers.ValidationError(msg)
                else:
                    msg = 'Invalid credentials'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Must provide username and password'
                raise serializers.ValidationError(msg)
            
            return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','is_active','is_staff','is_superuser']
        
        