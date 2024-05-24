from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from store.models import Product, Tag, Category, ProductItem, ProductItemImage, ProductAttribute


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ReadCategorySerializer(serializers.ModelSerializer):
    children = CategorySerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductItemImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductItemImage
        fields = '__all__'


class ImageForProductItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductItemImage
        exclude = ('product_item',)


class ItemForReadProductSerializer(serializers.ModelSerializer):

    images = ImageForProductItemSerializer(many=True)

    class Meta:
        model = ProductItem
        exclude = ('product',)


class ListProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    tags = TagSerializer(many=True)
    items = ItemForReadProductSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('content',)


class AttributeForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class DetailProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    tags = TagSerializer(many=True)
    items = ItemForReadProductSerializer(many=True)
    attributes = AttributeForProductSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ItemForCreateUpdateProductSerializer(WritableNestedModelSerializer):

    images = ImageForProductItemSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = ProductItem
        exclude = ('product',)


class CreateUpdateProductSerializer(WritableNestedModelSerializer):

    attributes = AttributeForProductSerializer(many=True)
    items = ItemForCreateUpdateProductSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class ProductItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductItem
        fields = '__all__'


class ProductForListProductItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('content',)


class ListProductItemSerializer(serializers.ModelSerializer):
    images = ImageForProductItemSerializer(many=True)
    product = ProductForListProductItemSerializer()

    class Meta:
        model = ProductItem
        fields = '__all__'


class ProductForDetailProductItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    attributes = AttributeForProductSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('content',)


class DetailProductItemSerializer(serializers.ModelSerializer):
    images = ImageForProductItemSerializer(many=True)
    product = ProductForDetailProductItemSerializer()

    class Meta:
        model = ProductItem
        fields = '__all__'


class CreateProductItemSerializer(WritableNestedModelSerializer):

    images = ImageForProductItemSerializer(many=True)

    class Meta:
        model = ProductItem
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = '__all__'
