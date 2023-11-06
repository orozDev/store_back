from django.utils.translation import gettext_lazy as _
from utils.models import TimeStampAbstractModel
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class Cart(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')
        ordering = ('-created_at', '-updated_at')

    first_name = models.CharField(_('имя'), max_length=50)
    last_name = models.CharField(_('фамилия'), max_length=50)
    address = models.CharField(_('адрес'), max_length=150)
    email = models.EmailField(_('почта'), null=False, blank=True)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name=_('номер телефона'))
    notes = models.CharField(_('заметки'), max_length=250)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    total_price.fget.short_description = _('итоговая цена')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class CartItem(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('товар заказа')
        verbose_name_plural = _('товары заказов')
        ordering = ('-created_at', '-updated_at')

    product = models.ForeignKey('store.Product', models.PROTECT, verbose_name=_('товар'))
    quantity = models.PositiveIntegerField(_('количество товаров'), default=1)
    cart = models.ForeignKey('order.Cart', models.CASCADE, 'items', verbose_name=_('заказ'))
    total_price = models.DecimalField(_('итоговая цена'), max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.cart}'

# Create your models here.
