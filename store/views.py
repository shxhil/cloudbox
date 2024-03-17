from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from store.serializers import UserSerializer,ProductSerializer,BasketItemSerializer,BasketSerializer

from rest_framework import viewsets
from store.models import Product,BasketItem,Basket

from rest_framework.decorators import action
from rest_framework import authentication,permissions

from rest_framework import serializers

# Create your views here.

class SignupView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data= serializer.data)
        else:
            return Response(data=serializer.errors)

    
class ProductsView(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["post"],detail=True)
    def add_to_basket(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        Product_object=Product.objects.get(id=id)
        basket_object=request.user.cart
        
        basket_products=request.user.cart.cartitem.all().values_list("product",flat=True)
        print(basket_products)
        if int(id) in basket_products:
            basket_item_object=BasketItem.objects.get(basket=basket_object,product__id=id)
            basket_item_object.quantity=basket_item_object.quantity+int(request.data.get("quantity",1))
            basket_item_object.save()
            serializer=BasketItemSerializer(basket_item_object)
            return Response(data=serializer.data)
        
        serializer=BasketItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=Product_object,basket=basket_object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission denied")
    
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission denied")

    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission denied")
    
    

class BasketView(viewsets.ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=request.user.cart
        #qs=Basket.objects.filter(owner=request.user) if no related name
        serializer=BasketSerializer(qs)
        return Response (data=serializer.data)


class BasketItemsView(viewsets.ModelViewSet):
    serializer_class=BasketItemSerializer
    queryset=BasketItem.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

#ee work ellam cheyyanath basket model ahn, ee basktitem  model use aakanath quantity more than one ulla th add aakan aahn
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def list(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def perform_update(self, serializer): #cheyth userkk mathree athil change cheyyan padollu 
         user=self.request.user #token pass akeetulla user
         owner=self.get_object().basket.owner #basket owner
               #basketitem.objects.get() another methord for get_object
         #self.get_object()=Basketitem model ahn indicate aakne, akatha basket -aa basket model nta akatha owner object
         if user == owner:
            return super().perform_update(serializer)
         else:
             raise serializers.ValidationError("owner permission denied")
         
    def perform_destroy(self, instance):
        user=self.request.user
        owner=self.get_object().basket.owner
        #or owner=instance.basket.owner
        if user == owner:
            return super().perform_destroy(instance)
        else:
             raise serializers.ValidationError("owner permission denied")
        















# o avoi duplicate products in cart
# class ProductsView(viewsets.ModelViewSet):
#     # ... (other methods remain unchanged)

#     @action(methods=["post"], detail=True)
#     def add_to_basket(self, request, *args, **kwargs):
#         id = kwargs.get("pk")
#         product_object = Product.objects.get(id=id)
#         basket_object = request.user.cart

#         # Check if the product is already in the basket
#         basket_item_object = BasketItem.objects.filter(basket=basket_object, product__id=id).first()

#         if basket_item_object:
#             # If the product is in the basket, update the quantity
#             basket_item_object.quantity += int(request.data.get("quantity", 1))
#             basket_item_object.save()
#             serializer = BasketItemSerializer(basket_item_object)
#             return Response(data=serializer.data)
#         else:
#             # If the product is not in the basket, create a new BasketItem
#             serializer = BasketItemSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(product=product_object, basket=basket_object)
#                 return Response(data=serializer.data)
#             else:
#                 return Response(data=serializer.errors)
