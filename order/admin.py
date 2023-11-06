from django.contrib import admin

from order.models import Cart, CartItem


class CartItemStackedInline(admin.StackedInline):
    model = CartItem
    extra = 1
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'first_name', 'phone', 'email',)
    list_display_links = ('id', 'first_name',)
    search_fields = ('id', 'first_name', 'last_name', 'address', 'email', 'phone', 'notes')
    inlines = (CartItemStackedInline,)
    readonly_fields = ('total_price', 'created_at', 'updated_at',)

# Register your models here.
