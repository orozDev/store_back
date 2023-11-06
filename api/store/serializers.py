from rest_framework import serializers

from store.models import Product, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_detail = TagSerializer(many=True, source='tags', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'