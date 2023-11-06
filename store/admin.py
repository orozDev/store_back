from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from store.models import Product, ProductImage, ProductAttribute, LinkedProduct, Category, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
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
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'get_image',)
    list_display_links = ('id', 'name',)
    list_editable = ('is_published',)
    list_filter = ('tags', 'category',)
    search_fields = ('name', 'description', 'content', 'price', 'color', 'attribute',)
    readonly_fields = ('get_full_image', 'created_at', 'updated_at',)
    inlines = (ProductImageStackedInline, ProductAttributeStackedInline,)
    form = ProductAdminForm

    @admin.display(description=_('изображение'))
    def get_image(self, obj):
        if self.image:
            return f'<img src="{obj.image.url}" alt="{obj.name}" width="150px">'
        return '-'

    @admin.display(description=_('изображение'))
    def get_full_image(self, obj):
        if self.image:
            return f'<img src="{obj.image.url}" alt="{obj.name}" width="75%">'
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


@admin.register(LinkedProduct)
class LinkedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'id',)
    list_filter = ('products',)
    readonly_fields = ('created_at', 'updated_at',)

# Register your models here.
