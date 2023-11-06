from django.contrib import admin
from django import forms
from core.models import Comment, CommentImage
from django.utils.translation import gettext_lazy as _


class CommentImageStackedInline(admin.StackedInline):
    model = CommentImage
    readonly_fields = ('created_at', 'updated_at',)
    extra = 1


class CommentAdminForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea(), label=_('Текст'))

    class Meta:
        model = Comment
        fields = '__all__'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'product',)
    list_display_links = ('id', 'name',)
    list_filter = ('product',)
    search_fields = ('id', 'name', 'email', 'text',)
    inlines = (CommentImageStackedInline,)
    readonly_fields = ('created_at', 'updated_at',)
    form = CommentAdminForm

# Register your models here.
