from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",default="default.jpg")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_trending=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


#baket nta akath items illa so we need to add Basketitms in it athin ahn ee methord kundvarne 
    @property #basket item thila object aayt serializer il kittan vendeet ahn @pro..
    def cart_items(self):
        #BasketItem.objects.filter(basket=self)  >> if there is no related name cartitem
        return self.cartitem.all() #here self means model basket
        
    
    
    @property
    def cart_item_quantity(self):
        qs=self.cart_items #cart nta akath ulla sanagal idkkan
        return qs.count()
    
    @property
    def sub_total(self):
        basket_items=self.cart_items
        total=0
        if basket_items:
            total_sum=sum([p.total for p in basket_items])
        return total_sum
    
class BasketItem(models.Model): #cart l more than one element add akaan ahn basket 2 nnam 
    basket=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def total(self):    #total price
        return self.quantity*self.product.price



#function
def create_basket(sender,instance,created,**kwargs):
    if created:#true or false
        Basket.objects.create(owner=instance)#instance=request.user
    
#signal=post_save
post_save.connect(create_basket,sender=User)
                                #user model l object creat avumma thanna basket creat avan aaayt=means user creat cheyyumma