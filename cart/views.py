from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})

@login_required
def index(request):
    template_data = {}
    template_data['title'] = 'Shopping Carts'
    
    # Get all carts for the user
    user_carts = Cart.objects.filter(user=request.user).order_by('cart_type')
    template_data['carts'] = user_carts
    
    # If a specific cart is selected, show its contents
    selected_cart_id = request.GET.get('cart_id')
    if selected_cart_id:
        try:
            selected_cart = Cart.objects.get(id=selected_cart_id, user=request.user)
            cart_items = CartItem.objects.filter(cart=selected_cart)
            
            cart_total = 0
            for item in cart_items:
                cart_total += item.movie.price * item.quantity
            
            template_data['selected_cart'] = selected_cart
            template_data['cart_items'] = cart_items
            template_data['cart_total'] = cart_total
        except Cart.DoesNotExist:
            messages.error(request, 'Cart not found.')
    
    return render(request, 'cart/index.html', {'template_data': template_data})

@login_required
def add(request, id):
    movie = get_object_or_404(Movie, id=id)
    cart_type = request.POST.get('cart_type', 'cart1')
    quantity = int(request.POST.get('quantity', 1))
    
    # Get or create the cart
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        cart_type=cart_type,
        defaults={'cart_type': cart_type}
    )
    
    # Get or create the cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        movie=movie,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'Added {movie.name} to {cart.get_cart_type_display()}')
    return redirect('movies.show', id=id)

@login_required
def clear_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    messages.success(request, f'Cleared {cart.get_cart_type_display()}')
    return redirect('cart.index')

@login_required
def remove_item(request, cart_id, item_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.success(request, f'Removed {cart_item.movie.name} from {cart.get_cart_type_display()}')
    return redirect(f'{reverse("cart.index")}?cart_id={cart_id}')

@login_required
def checkout(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        messages.error(request, 'Cart is empty')
        return redirect('cart.index')
    
    # Calculate total
    total = 0
    for item in cart_items:
        total += item.movie.price * item.quantity
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        total=total
    )
    
    # Create order items
    for item in cart_items:
        Item.objects.create(
            movie=item.movie,
            price=item.movie.price,
            quantity=item.quantity,
            order=order
        )
    
    # Clear the cart
    cart_items.delete()
    
    messages.success(request, f'Order #{order.id} created successfully!')
    return redirect(f'{reverse("cart.purchase")}?order_id={order.id}')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')
# Create your views here.
