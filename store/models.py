from django.db import models

# Collection - Product
# Customer - Order
# Order - Item
# Cart - Item
# Create your models here.


class Promotion(models.Model):
  description = models.CharField(max_length=255)
  discount = models.FloatField()


class Collection(models.Model):
  title = models.CharField(max_length=255)
  featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
  


class Product(models.Model):
  title = models.CharField(max_length=255)
  # slug = models.SlugField(default='-')
  slug = models.SlugField(null=True)
  description = models.TextField()
  # 9999.99
  price = models.DecimalField(max_digits=6, decimal_places=2)
  inventory = models.IntegerField()
  last_update = models.DateTimeField(auto_now=True)
  collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
  promotions = models.ManyToManyField(Promotion, related_name='products')

class Order(models.Model):
  PAYMENT_PENDING = 'P'
  PAYMENT_COMPLETE = 'C'
  PAYMENT_FAILED = 'F'
  
  PAYMENT_STATUS = [
    (PAYMENT_PENDING, 'Pending'),
    (PAYMENT_COMPLETE, 'Complete'),
    (PAYMENT_FAILED, 'Failed')
  ]
  placed_at = models.DateTimeField(auto_now_add=True)
  payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_PENDING)
  customer = models.ForeignKey('Customer', on_delete=models.PROTECT, related_name='customr_order')


class Customer(models.Model):
  MEMBERSHIP_BRONZE = 'B'
  MEMBERSHIP_SILVER = 'S'
  MEMBERSHIP_GOLD = 'G'
  
  MEMBERSHIP_CHOICES = [
    (MEMBERSHIP_BRONZE, 'Bronze'),
    (MEMBERSHIP_SILVER, 'Silver'),
    (MEMBERSHIP_GOLD, 'Gold'),
  ]
  
  # MEMBERSHIP_CHOICES = [
  #   ('B', 'Bronze'),
  #   ('S', 'Silver'),
  #   ('G', 'Gold'),
  # ]
  
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=255)
  birth_date = models.DateField(null=True)
  # membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')
  membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_custumor')
  class Meta:
    # db_table = 'store_customers'
    indexes = [
      models.Index(fields=['last_name', 'first_name'])
    ]


class Cart(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveSmallIntegerField()


class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.PROTECT)
  quantity = models.PositiveSmallIntegerField()
  unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
  # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, primary_key=True)

