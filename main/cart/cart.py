from shop.models import Product

CART_SESSION_KEY = 'cart'


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)

        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        product.id = str(product.id)
        if product.id not in self.cart:
            self.cart[product.id] = {'quantity': 0}
        if override_quantity:
            self.cart[product.id]['quantity'] = quantity
        else:
            self.cart[product.id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product.id = str(product.id)
        if product.id in self.cart:
            del self.cart[product.id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.save()

    def get_total_price(self):
        return sum(item['total_price'] for item in self)

    def __len__(self):
        return sum([item['quantity'] for item in self.cart.values()])

    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart.keys(), available=True)

        for product in products:
            quantity = self.cart[str(product.id)]['quantity']
            yield {
                'product': product,
                'quantity': quantity,
                'total_price': quantity * product.price,
                'price': product.price,
            }