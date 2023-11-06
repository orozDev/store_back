from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import TimeStampAbstractModel
from django_resized import ResizedImageField


class Comment(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('комментарии')
        verbose_name_plural = _('комментарии')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('Имя и фамилия'), max_length=100)
    email = models.EmailField(_('электронная почта'))
    text = models.CharField(_('текст'), max_length=300)
    product = models.ForeignKey('store.Product', models.CASCADE, verbose_name=_('продукт'))

    def __str__(self):
        return f'{self.name} - {self.email}'


class CommentImage(TimeStampAbstractModel):

    class Meta:
        verbose_name = _('изображение комментария')
        verbose_name_plural = _('изображении комментариев')
        ordering = ('-created_at', '-updated_at')

    image = ResizedImageField(upload_to='comment_images/', force_format='WEBP', quality=90,
                              verbose_name=_('изображение'),
                              null=True, blank=True)
    comment = models.ForeignKey('core.Comment', models.CASCADE, 'images', verbose_name=_('комментарии'))

    def __str__(self):
        return f'{self.comment.name}'

# Create your models here.
