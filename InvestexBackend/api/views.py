from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import Share
from .serializers import ShareSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Generate or get the token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_login(request):
    return Response({'status': 'User is logged in'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def share_list_create(request):
    if request.method == 'GET':
        shares = Share.objects.filter(user=request.user)
        serializer = ShareSerializer(shares, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = ShareSerializer(data=request.data)
        print(serializer)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def share_detail(request, pk):
    try:
        share = Share.objects.get(pk=pk, user=request.user)
    except Share.DoesNotExist:
        return Response({'error': 'Share not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShareSerializer(share)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShareSerializer(share, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        share.delete()
        return Response({'message': 'Share deleted successfully'}, status=status.HTTP_204_NO_CONTENT)