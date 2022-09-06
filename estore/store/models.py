from django.db import models
# django models give the basic structure of the tables in the database and the
# relationship between the tables

# Customer/User - imported from django's prebuilt User model
from django.contrib.auth.models import User

# Shipping Address - The address is tied to a user
# Foreign key - defines a relationship between tables
# on_delete=models.CASCADE - delete info related to this user. For instance, if the user gets
# then the user's cart, address, etc, gets deleted as well

class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    location = models.CharField(max_length=150, verbose_name="Location")
    street_address = models.CharField(max_length=200, verbose_name="Street Address")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")

    def __str__(self):
        return self.location

# Category - distinguish between products and helps in organizing/filtering the website
# is_active lets us hide the product category completely from website
# is_featured lets us hide the product category from the home page
class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.CharField(max_length=100, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to="category", blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ('-created_at', )

    # Image property - implemented with try except block to prevent page from crashing if a product image is missing
    # @property   
    # def imageURL(self):
    #     try:
    #         url = self.image.url
    #     except:
    #         url = ''
    #     return url

    def __str__(self):
        return self.title

# Product - elements/info that each product in the eStore needs to have, similar to the
# category class this includes basic information such as the name/tile, description, image
# as well as more specific information such as the price. 
# Each item should also have a category - (foreign key!) 
class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Product Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=200, verbose_name="Product Slug")
    sku = models.CharField(max_length =100, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to="product", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = "Products"
        ordering = ('-created_at', )

    # Image property - implemented with try except block to prevent page from crashing if a product image is missing
    # @property   
    # def imageURL(self):
    #     try:
    #         url = self.image.url
    #     except:
    #         url = ''
    #     return url
    
    def __str__(self):
        return self.title

# Cart - When purchasing items, users will add cart items to their order
# each cart item is responsible for one type of product but can have varying quantities
# of that item, depending on how much the user wishes to purchase
class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)
    
    # total price property of the cart item
    @property
    def total_price(self):
        return self.quantity * self.product.price

 # different states that the order is currently in
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

# Order - Keeps track of a user's order and the different status of that order
class Order(models.Model):
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Pending")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")

