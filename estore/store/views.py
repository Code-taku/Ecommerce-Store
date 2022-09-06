# from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Address, Category, Product, Cart, Order
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Views - python functions which receive a web request and return a web response
#         (similar to Node.js's Express routers)


# Home Page
def home(request):
    # filter based on which categories and products are active AND marked to be featured on homepage
    # up to 3 categories and up to 8 products
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        "categories" : categories,
        "products" : products,
    }
    return render(request, "store/index.html", context)

# Detail Page for a specific Product based on slug; also renders related products to the customer
def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # related products are of the same category but not including the current product in detail
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        "product" : product,
        "related_products" : related_products,
    }
    return render(request, "store/detail.html", context)

# Display all active categories in our eStore
def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "store/categories.html", {'categories' : categories})

# Display all products of a specific category
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    context = {
        "category" : category,
        "products" : products,
        "categories" : categories,
    }
    return render(request, "store/category_products.html", context)

# Authentication

# Register a new customer, class-based view
class RegistrationView(View):
    form_class = RegistrationForm()
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, "Welcome to the Club! Registration Successful.")
            form.save()
        return render(request, self.template_name, {'form' : form})

# View User Profile (must be logged in)
@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, "account/profile.html", {'addresses' : addresses, 'orders' : orders})

# View User's Address Page (must be logged in)
@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, "account/add_address.html", {'form' : form})
    
    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            location = form.cleaned_data['location']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            address = Address(user=user, location=location, street_address=street_address, city=city, state=state)
            address.save()
            messages.success(request, "New Address Added Successfully")
        return redirect('store:profile')

# Remove an existing address from profile (must be logged in)
@login_required
def remove_address(request, id):
    to_remove = get_object_or_404(Address, user=request.user, id=id)
    to_remove.delete()
    messages.success(request, "Address Successfully Removed")
    return redirect('store:profile')

# View User's Cart (must be logged in)
# Each of a user's 'cart' only corresponds to one product since the role of the cart is to keep track
# of the products' quantity and the total price for that particular product. Thus a user buying multiple
# products will have multiple cart items

@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total Price
    cart_cost = decimal.Decimal(0)
    shipping_cost = decimal.Decimal(10) # default shipping cost is $10
    for cart_product in cart_products:
        cart_cost += cart_product.total_price

    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products' : cart_products,
        'cart_cost' : cart_cost,
        'shipping_cost' : shipping_cost,
        'total_cost' : cart_cost + shipping_cost,
        'addresses' : addresses,
    }

    return render(request, 'store/cart.html', context)


# Add a new item to cart - performed from store view (must be logged in) 
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is already in the cart or not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    # if in cart already, increment quantity
    if item_already_in_cart:
        item = get_object_or_404(Cart, product=product_id, user=user)
        item.quantity += 1
        item.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('store:cart')

# Edit cart functions performed from cart view

# Entirely remove an existing item from cart (must be logged in)
@login_required
def remove_from_cart(request, cart_id):
    if request.method == 'GET':
        to_remove = get_object_or_404(Cart, id=cart_id)
        to_remove.delete()
        messages.success(request, "Product Removed from Cart")
    return redirect('store:cart')

# Increment the quantity of an existing item in cart (must be logged in)
@login_required
def incr_cart_item(request, cart_id):
    if request.method == 'GET':
        to_incr = get_object_or_404(Cart, id=cart_id)
        to_incr.quantity += 1
        to_incr.save()
    return redirect('store:cart')

# Decrement the quantity of an existing item in cart (must be logged in)
@login_required
def decr_cart_item(request, cart_id):
    if request.method == 'GET':
        to_decr = get_object_or_404(Cart, id=cart_id)
        # remove if only 1 left
        if to_decr.quantity == 1:
            to_decr.delete()
        else:
            to_decr.quantity -= 1
            to_decr.save()
    return redirect('store:cart')

# Checking out all products in cart
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')

    address = get_object_or_404(Address, id=address_id)

    cart = Cart.objects.filter(user=user)
    for cart_item in cart:
        # Saving all products in cart to order
        Order(user=user, address=address, product=cart_item.product, quantity=cart_item.quantity).save()
        # Delete cart item after done processing it
        cart_item.delete()
    return redirect('store:orders')

# View all orders
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'store/orders.html', {'orders' : all_orders})

def shop(request):
    return render(request, 'store/shop.html')
    