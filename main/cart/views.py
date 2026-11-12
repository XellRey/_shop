from typing import override

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product

from .cart import Cart

# Create your views here.

MAX_QUANTITY = 99

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)

    try:
        quantity = int(request.POST.get('quantity', '1'))
    except ValueError:
        quantity = 1
    quantity = min(max(quantity, 1), MAX_QUANTITY)

    override = request.POST.get('override') == '1'
    cart.add(product, quantity, override_quantity=override)
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

