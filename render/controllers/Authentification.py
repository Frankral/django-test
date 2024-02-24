from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
from datetime import datetime, timedelta
SECRET_KEY = 'costhunAmblavao'
@api_view(['GET', 'POST'])
def Login(request):
    if request.method == 'POST':
        # request_data = json.loads(request.body)
        # username = request_data.get('username')
        # password = request_data.get('password')
        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     return JsonResponse({
        #         'error': 'Invalid username',
        #         'status': 400,
        #         'message': 'Bad request'
        #         }, status=status.HTTP_400_BAD_REQUEST)
        
        # if user.check_password(password):
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode(
            {
                'user_id': 'user.id',
                'username': 'user.username',
                'email': 'user.email',
                'exp': expiration_time,
            },
            SECRET_KEY,
            algorithm='HS256' 
        )
        return Response({'user_info': token}, status=status.HTTP_200_OK)
        # return JsonResponse({
        #     'error': 'Invalid password',
        #     'status': 400,
        #     'message': 'Bad request'
        #     }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Decode (request):
    if request.method == 'POST':
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTIzIiwidXNlcm5hbWUiOiJqb2huX2RvZSIsImVtYWlsIjoiam9obi5kb2VAZXhhbXBsZS5jb20iLCJleHAiOjE3MDgwOTM3MTJ9.vU6Ye9k-5SY61Et3QTlKk96Hl3AXvfDqeR0HTIG3n9A"

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_info = {
                'user_id': decoded_token['user_id'],
                'username': decoded_token['username'],
                'email': decoded_token['email'],
            }
            return Response({'user_info': user_info}, status=status.HTTP_200_OK)
        except Exception as e:
    
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)