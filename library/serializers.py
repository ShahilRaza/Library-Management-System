from rest_framework import serializers
from .models import User
from .models import Book
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import encrypt_text



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='normal')
    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")

    def create_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role 
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }




class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year', 'encrypted_isbn', 'genre', 'availability']
        read_only_fields = ['encrypted_isbn']



class BookCreateSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(write_only=True)
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'genre', 'availability']

    def create(self, validated_data):
        isbn = validated_data.pop('isbn')
        validated_data['encrypted_isbn'] = encrypt_text(isbn)
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'isbn' in validated_data:
            isbn = validated_data.pop('isbn')
            instance.encrypted_isbn = encrypt_text(isbn)
        return super().update(instance, validated_data)
