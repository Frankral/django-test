from django.urls import path
from .controllers.Authentification import Login, Decode, Signup
from .controllers.Uploadfile import Upload
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', Login, name='get-token'),
    path('verify', Decode, name='verify-token'),
    path('register', Signup, name='sing up'),
    path('upload/<id>', Upload, name='upload file'),
]