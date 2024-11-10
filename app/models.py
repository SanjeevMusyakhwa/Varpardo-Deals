from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  full_name = models.CharField(max_length=200)
  address = models.CharField(max_length=200, null=True, blank=True)
  joined_on = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.full_name
  

class Category(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField(unique=True)

  def __str__(self):
    return self.title


class Product(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField(unique=True)
  category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
  is_available = models.BooleanField(default=True)  
  image = models.ImageField(upload_to='products')
  marked_price = models.PositiveIntegerField()
  selling_price = models.PositiveIntegerField()
  description = models.TextField()
  warranty = models.CharField(max_length=200)
  return_policy = models.CharField(max_length=300, null=True, blank=True)
  view_count = models.PositiveIntegerField(default=0)

  def __str__(self):
    return self.title
  
  def get_discount_percentage(self):
    discount = (self.marked_price - self.selling_price) / self.marked_price * 100
    return discount

  
class Cart(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  total = models.PositiveIntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Cart : {self.id}"
  
class CartProduct(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  rate = models.PositiveIntegerField()
  subtotal = models.PositiveIntegerField()
  quantity = models.PositiveIntegerField(default=0)

  def __str__(self):
    return f"Cart: {self.cart.id} with Cart Product : {self.id}"
  

ORDER_STATUS = (
  ('Order Received','Order Received'),
  ('Order Processing','Order Processing'),
  ('Order on the way','Order on the way'),
  ('Order Completed','Order Completed'),
  ('Order Canceled','Order Canceled'),
)
class Order(models.Model):
  cart = models.OneToOneField(Cart,on_delete=models.CASCADE)
  ordered_by = models.CharField(max_length=200)
  shipping_address = models.CharField(max_length=200)
  mobile = models.CharField(max_length=10)
  email = models.EmailField(null= True,blank=True)
  subtotal = models.PositiveIntegerField()
  discount = models.PositiveIntegerField()
  total = models.PositiveIntegerField()
  order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Order: {self.id}"



 
