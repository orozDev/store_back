from rest_framework import serializers

from core.models import Comment, CommentImage
from store.models import Product


class ProductCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
        )


class CommentImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentImage
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    product_detail = ProductCommentSerializer(source='product', read_only=True, many=False)
    images = CommentImageSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = '__all__'