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
