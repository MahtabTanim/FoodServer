from marketplace.models import Cart, Tax


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
    total = 0.0
    subtotal = 0
    total = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cart in cart_items:
                subtotal += (cart.quantity) * (cart.fooditem.price)
        except:
            total = 0
            subtotal = 0

    tax, tax_dict = get_tax_on_total(subtotal)
    total = subtotal + tax
    return dict(subtotal=subtotal, total=total, tax=tax, tax_dict=tax_dict)


def get_tax_on_total(subtotal):
    taxes = Tax.objects.filter(is_active=True)
    tax_dict = {}
    total_percentage = 0
    for t in taxes:
        total_percentage += t.tax_percentage
        tax_dict.update(
            {
                t.tax_type: {
                    str(t.tax_percentage): str(
                        round((subtotal * t.tax_percentage) / 100, 2)
                    )
                }
            }
        )
    return round((subtotal * total_percentage) / 100, 2), tax_dict
