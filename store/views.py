from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from store.serializers import UserSerializer,ProductSerializer

from rest_framework import viewsets
from store.models import Product

# Create your views here.

class SignupView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data= serializer.data)
        else:
            return Response(data=serializer.errors)

class productsView(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    
