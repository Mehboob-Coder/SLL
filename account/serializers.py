       

from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'profile_pic', 'file', 'Reg_id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')          
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            profile_pic=validated_data['profile_pic'],
            file=validated_data['file'],
            Reg_id=validated_data.get('Reg_id', None),
        )
        user.set_password(password)  
        user.save()
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return {
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'profile_pic': user.profile_pic,
            'file': user.file,
            'Reg_id': user.Reg_id,
            'token': token.key,
            "message": "User registered successfully."
        }

