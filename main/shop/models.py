from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField('name', unique=True, max_length=100)
    slug = models.SlugField('slug', unique=True, max_length=100)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    #PROTECT - нельзя будет удалить категорию, пока в ней есть товары
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products',
                                 verbose_name="category")
    name = models.CharField('name', max_length=100)
    slug = models.SlugField('slug', unique=True, max_length=100)
    description = models.TextField('description', blank=True)
    price = models.DecimalField('price', max_digits=10, decimal_places=2)
    image = models.ImageField('image', upload_to='products/%Y/%m', blank=True)
    available = models.BooleanField('available', default=True)
    created_at = models.DateTimeField('created',auto_now_add=True)
    updated_at = models.DateTimeField('updated',auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['available', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Адрес страницы товара"""
        return reverse('shop:product', args=[self.slug])
