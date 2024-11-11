from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Book
from .serializers import BookSerializer, BookCreateSerializer
from .utils import decrypt_text
from rest_framework.permissions import AllowAny
from django.conf import settings



@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']  
        token_data = serializer.create_jwt_token(user) 
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    if request.user.role != 'admin':
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    serializer = BookCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Book created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([AllowAny])
def read_book(request,id):
    try:
        book = Book.objects.get(id=id)
        data = BookSerializer(book).data
        data['isbn'] = decrypt_text(book.encrypted_isbn)
        return Response(data, status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_book(request, id):
    if request.user.role != 'admin':
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    try:
        book = Book.objects.get(id=id)
        serializer = BookCreateSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book updated successfully","updated_data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book(request, id):
    if request.user.role != 'admin':
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
@permission_classes([AllowAny])
def filter_books(request):
    author = request.query_params.get('author')
    genre = request.query_params.get('genre')
    availability = request.query_params.get('availability')
    publication_year = request.query_params.get('publication_year')
    start_year = request.query_params.get('start_year')
    end_year = request.query_params.get('end_year')
    books = Book.objects.all()

    if author:
        books = books.filter(author=author)
    if genre:
        books = books.filter(genre=genre)
    if availability is not None:
        books = books.filter(availability=(availability.lower() == 'true'))
    if publication_year:
        try:
            books = books.filter(publication_year=int(publication_year))
        except ValueError:
            return Response({"error": "Invalid publication year"}, status=status.HTTP_400_BAD_REQUEST)
    if start_year and end_year:
        books = books.filter(publication_year__range=(int(start_year), int(end_year)))
        
    serialized_books = BookSerializer(books, many=True).data
    for book in serialized_books:
        book['isbn'] = decrypt_text(book['encrypted_isbn'])
    return Response(serialized_books, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def count_books_by_genre(request, genre):
    count = Book.objects.filter(genre=genre).count()
    return JsonResponse({'genre': genre, 'count': count})




@api_view(['GET'])
@permission_classes([AllowAny])
def recent_books(request):
    books = Book.objects.all().order_by('-id')[:5]
    serialized_books = BookSerializer(books, many=True).data
    for book in serialized_books:
        book['isbn'] = decrypt_text(book['encrypted_isbn'])
    return Response(serialized_books, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def books_by_author_sorted(request, author):
    books = Book.objects.filter(author=author).order_by('publication_year')
    serialized_books = BookSerializer(books, many=True).data
    for book in serialized_books:
        book['isbn'] = decrypt_text(book['encrypted_isbn'])
    return Response(serialized_books, status=status.HTTP_200_OK)


