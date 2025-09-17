from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializer import UsuarioSerializer
import requests

@api_view({"GET","POST"})
def usuario_list_create(request):
        if request.method == "GET":
            
            usuarios = Usuario.objects.all()
            serializer = UsuarioSerializer(usuarios, many=True)
            return Response(serializer.data)
        
        if request.method == "POST":
              
            serializer = UsuarioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view({"GET","PUT","DELETE"})
def usuario_detail(request,pk):
    try:
        usuario = Usuario.objects.all(pk=pk)
    except Usuario.DoesNotExist:
         return Response({'error': 'Usuário não encontrato'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        usuario.delete()
        return Response({"message": "Usuario Deletado"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view({"POST"})
def random_user(request):
    try:
        response = request.get("https://randomuser.me/api/", timeout=5)
        data = response.json()
        random_user = data['results'][0]

        new_user = {
            'nome' : f"{random_user['name']['primeiro']} {random_user ['name'] ['ultimo']}", 
            "email" : random_user ['email'], 
            'idade' : random_user ['idade'],
        }
        serializer = UsuarioSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)