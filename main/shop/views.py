from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product


# Create your views here.

def index(request, category_slug=None):
    ''' Показывает список товаров которые в наличии.

        Без category_slug покажет весь список,
        с ним только товары из категории '''

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    data = {
        'categories': categories,
        'products': products,
        'category': category,
    }
    return render(request, 'shop/index.html', data)