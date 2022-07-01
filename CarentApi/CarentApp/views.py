from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from CarentApp.models import User
from rest_framework.decorators import action
from .serializers import UserSerializer
from django.contrib.auth.models import AnonymousUser
# Create your views here.


class UserView(viewsets.ViewSet):
    def list(self,request):
        if(request.user != AnonymousUser()):
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user,many=False)
            return Response(serializer.data)
        else:
            return Response(status=401)
