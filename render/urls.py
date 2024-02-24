from django.urls import path
from .controllers.Authentification import Login, Decode
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', Login, name='get-token'),
    path('verify', Decode, name='verify-token'),
]