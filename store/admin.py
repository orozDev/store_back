from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from store.models import Product, ProductItemImage, ProductAttribute, Category, Tag, ProductItem
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe


class ProductImageStackedInline(admin.StackedInline):
    model = ProductItemImage
    extra = 1
    readonly_fields = ('created_at', 'updated_at',)


class ProductAttributeStackedInline(admin.StackedInline):
    model = ProductAttribute
    extra = 1
    readonly_fields = ('created_at', 'updated_at',)


class ProductAdminForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(), label=_('Описание'))
    content = forms.CharField(widget=CKEditorUploadingWidget(), label=_('Описание'))

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_published', 'user', 'get_image',)
    list_display_links = ('id', 'name',)
    list_editable = ('is_published',)
    list_filter = ('tags', 'category', 'user')
    search_fields = ('name', 'description', 'content', 'items_color', 'items_attribute',)
    readonly_fields = ('get_full_image', 'created_at', 'updated_at',)
    inlines = (ProductAttributeStackedInline,)
    form = ProductAdminForm
    raw_id_fields = ('category', 'user')
    filter_horizontal = ('tags',)

    @admin.display(description=_('изображение'))
    def get_image(self, obj):
        image = obj.items.first()
        if image:
            return mark_safe(f'<img src="{image.image.url}" alt="{obj.name}" width="150px">')
        return '-'

    @admin.display(description=_('изображение'))
    def get_full_image(self, obj: Product):
        image = obj.items.first()
        if image:
            return mark_safe(f'<img src="{image.image.url}" alt="{obj.name}" width="75%">')
        return '-'


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product', 'color', 'price', 'get_image')
    list_filter = ('product__category', 'product__tags', 'product__is_published')
    search_fields = ('name', 'product__name', 'product__description', 'product__content')
    readonly_fields = ('get_full_image', 'created_at', 'updated_at',)
    inlines = (ProductImageStackedInline,)
    raw_id_fields = ('product',)

    @admin.display(description=_('изображение'))
    def get_image(self, obj: ProductItem):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" alt="{obj.name}" width="150px">')
        return '-'

    @admin.display(description=_('изображение'))
    def get_full_image(self, obj: ProductItem):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" alt="{obj.name}" width="75%">')
        return '-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent',)
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'id',)
    list_filter = ('parent',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'id',)
    readonly_fields = ('created_at', 'updated_at',)


# Register your models here.
