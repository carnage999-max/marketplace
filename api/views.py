from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)


def ApiOverview(request):
    return JsonResponse('All API endpoints', safe=False)

@api_view(['GET', 'POST'])
def getusers(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)