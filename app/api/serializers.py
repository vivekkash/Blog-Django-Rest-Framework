from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from . models import Blog


class UserSerializer(serializers.ModelSerializer):
    blogs = serializers.PrimaryKeyRelatedField(many=True, queryset=Blog.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'blogs']
        
        

class RegisterUserSerializer(serializers.Serializer):

        first_name = serializers.CharField(max_length=50)
        last_name = serializers.CharField(max_length=50)
        username = serializers.CharField(max_length=50)
        password = serializers.CharField(max_length=30)
        
        
        def validate(self, data):
            
            if User.objects.filter(username=data.get('username')).exists():
                raise serializers.ValidationError('Username name already taken')
            
            return data
        
        def create(self, validated_data):

            User.objects.create_user(first_name=validated_data.get('first_name'), 
                                       last_name=validated_data.get('last_name'),
                                       username=validated_data.get('username'),
                                       password=validated_data.get('password')
                                       )
                                
            return validated_data
        
        
class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    password = serializers.CharField()
    
    
    def validate(self, data):
        
        if User.objects.filter(username=data.get('username')).exists():
            return data
        
        raise serializers.ValidationError('Username is not registered')
        
        
    def get_jwt_token(self, data):
        
        user = authenticate(username=data.get('username'), password=data.get('password'))
        
        print("user ",user)
        
        if user:
            
            return RefreshToken.for_user(user)
        
        else: 
            
            return False;    
        
        
class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Blog
        exclude=['created_at', 'updated_at']
        
        
            
                    
        