from rest_framework import serializers

from core.models import Comment, CommentImage
from utils.serializers import ShortDescUserSerializer


class CommentImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentImage
        fields = '__all__'


class ImageForCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentImage
        exclude = ('comment',)


class ReadCommentSerializer(serializers.ModelSerializer):

    user = ShortDescUserSerializer()
    images = ImageForCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    images = ImageForCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)