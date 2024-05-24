from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from utils.models import TimeStampAbstractModel
from django_resized import ResizedImageField


class ProductAttribute(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('Атрибут товаров')
        verbose_name_plural = _('Атрибуты товаров')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('название'), max_length=50)
    value = models.CharField(_('значение'), max_length=50)
    product = models.ForeignKey('store.Product', models.CASCADE, 'attributes', verbose_name=_('товар'))

    def __str__(self):
        return f'{self.name} {self.product.name}'


class Product(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('название продукта'), max_length=100)
    description = models.CharField(_('описание'), max_length=255)
    content = models.TextField(_('контент'))
    category = models.ForeignKey('store.Category', models.PROTECT, verbose_name=_('категория'))
    tags = models.ManyToManyField('store.Tag', verbose_name=_('теги'))
    is_published = models.BooleanField(_('публичность'), default=False)
    user = models.ForeignKey('account.User', models.CASCADE, verbose_name=_('пользователь'))

    # @property
    # def products(self):
    #     return self.linked_products.first().products.exlude(id=self.id)

    def __str__(self):
        return f'{self.name}'


class ProductItem(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('ассортимент товар')
        verbose_name_plural = _('ассортименты товаров')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('название'), max_length=120, null=True, blank=True)
    color = models.CharField(_('цвет (HEX)'), max_length=120, null=True, blank=True)
    price = models.DecimalField(_('цена'), decimal_places=2, max_digits=7)
    product = models.ForeignKey('store.Product', models.CASCADE, related_name='items', verbose_name=_('товар'))

    @property
    def full_name(self):
        return f'{self.product.name} {self.name}'

    @property
    def image(self):
        images = self.images.filter(is_main=True)
        if images.exists():
            return images.first().image
        return self.images.first().image


# class LinkedProduct(TimeStampAbstractModel):
#
#     class Meta:
#         verbose_name = _('Связь продуктов')
#         verbose_name_plural = _('Связи продуктов')
#         ordering = ('-created_at', '-updated_at')
#
#     name = models.CharField(_('название'), max_length=100, default='')
#     products = models.ManyToManyField('store.Product', 'linked_products', verbose_name=_('товары'))
#
#     def __str__(self):
#         return f'{self.name}'
#
#     def clean(self):
#         linked_products = LinkedProduct.objects.filter(products__in=self.products)
#         if linked_products.exists():
#             raise ValidationError({'products': [_('Один из продуктов уже имеет связь')]})


class Category(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('название'), max_length=100, unique=True)
    parent = models.ForeignKey('self', models.SET_NULL, 'children',
                               verbose_name=_('родительская категория'), blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def is_parent(self):
        return self.parent is not None


class Tag(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('тег')
        verbose_name_plural = _('теги')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('название'), max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class ProductItemImage(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('изображение продукта')
        verbose_name_plural = _('изображение продуктов')
        ordering = ('-created_at', '-updated_at')

    image = ResizedImageField(upload_to='products_images/', force_format='WEBP', quality=90, verbose_name=_('изображение'),
                              null=True, blank=True)
    is_main = models.BooleanField(_('заголовочное изображение'), default=False)
    product_item = models.ForeignKey('store.ProductItem', models.CASCADE, 'images', verbose_name=_('товар'))

    def __str__(self):
        return f'{self.product_item.full_name}'

    def clean(self):
        if self.is_main:
            product_images = ProductItemImage.objects.filter(product_item=self.product_item, is_main=True)
            if product_images.exists():
                raise ValidationError({'is_main': [_('Только одна картина может быть главным')]})

# Create your models here.
