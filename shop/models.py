from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    product_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    desc=models.CharField(max_length=300)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    pub_date=models.DateField()
    image=models.ImageField(upload_to='shop/images',default="")

    def __str__(self):
        return self.title            #in the admin page in the list of products name of the product will be displayed instead of default names
    
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)   # When null=True is set on a model field, it means that the field is allowed to store NULL values in the database.
    name=models.CharField(max_length=200,null=True)                                 #When blank=True is set on a model field, it means that the field is allowed to be empty in forms.
    email=models.EmailField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True) #references the primary key of customer model which is a id that is assigned automatically when the customer is created
    date_ordered=models.DateTimeField(auto_now_add=True)  #Automatically sets this field to the current date and time when the order is first created.
    complete=models.BooleanField(default=False,null=True,blank=False)   #if a order is complete items are added to new cart  
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_quantity(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product=models.ForeignKey(product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property   #by using property decorator we can make functions behave like attributes
    def get_total(self):
        total=self.product.price* self.quantity
        return total

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


    
