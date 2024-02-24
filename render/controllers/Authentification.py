from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
from datetime import datetime, timedelta
from render.models import User
from render.serializers import UserSerializer

SECRET_KEY = '!&costhunt2024'

@api_view(['GET', 'POST'])
def Login(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        username = request_data.get('username')
        password = request_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'Invalid username',
                'status': 400,
                'message': 'Bad request'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(password):
            expiration_time = datetime.utcnow() + timedelta(seconds=20)
            token = jwt.encode(
                {
                    'username': user.username,
                    "name": user.name,
                    'email': user.email,
                    'isAdmin': True,
                    'exp': expiration_time,
                },
                SECRET_KEY,
                algorithm='HS256' 
                )
            return Response({'user_info': token}, status=status.HTTP_200_OK)
        return JsonResponse({
            'error': 'Invalid password',
            'status': 400,
            'message': 'Bad request'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Decode (request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        token = request_data.get('token')
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return Response({'user_info': decoded_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def Signup (request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        serializerUser = UserSerializer(data=request_data)
        if serializerUser.is_valid():
            user = serializerUser.save()
            expiration_time = datetime.utcnow() + timedelta(seconds=20)
            token = jwt.encode(
                {
                    'username': user.username,
                    "name": user.name,
                    'email': user.email,
                    'exp': expiration_time,
                },
                SECRET_KEY,
                algorithm='HS256' 
                )
            response_data = UserSerializer(user).data
            response_data["token"] = token
            return Response(response_data, status=status.HTTP_201_CREATED)
        return JsonResponse({'errors': serializerUser.errors}, status=status.HTTP_400_BAD_REQUEST)