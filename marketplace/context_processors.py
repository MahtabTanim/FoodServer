from marketplace.models import Cart


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cart in cart_items:
                cart_count += cart.quantity
        except:
            cart_count = 0
    return {"cart_count": cart_count}


def get_cart_total(request):
    total = 0
    subtotal = 0
    tax = 10
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cart in cart_items:
                subtotal += (cart.quantity) * (cart.fooditem.price)
            total = subtotal + tax
        except:
            total = 0
            subtotal = 0
            tax = 0
    return dict(subtotal=subtotal, total=total, tax=tax)
