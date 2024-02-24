from rest_framework.decorators import api_view
import os
from django.conf import settings
from django.http import JsonResponse
from render.models import User
from rest_framework.response import Response
from rest_framework import status

@api_view(['PUT'])
def Upload (request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' and request.FILES.get('image'):
        image_file = request.FILES['image']
        storage_directory = os.path.join(settings.MEDIA_ROOT, 'images/profiles/')
        if user.image and user.image != "/images/profiles/default.jpg":
            previous_image_path = os.path.join(settings.MEDIA_ROOT, str(user.image).lstrip('/'))
            print(previous_image_path)
            if os.path.exists(previous_image_path):
                os.remove(previous_image_path)            
        if not os.path.exists(storage_directory):
            os.makedirs(storage_directory)
        
        image_name = f"{user.username}_profile_image{os.path.splitext(image_file.name)[1]}"
        image_path = os.path.join(storage_directory, image_name)
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        user_path = f'/images/profiles/{image_name}'
        user.image = user_path
        user.save()
        return JsonResponse({'path': user.image}, status=201)

    return JsonResponse({'error': 'Bad request'}, status=400)
   
