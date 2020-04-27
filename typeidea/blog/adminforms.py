from dal import autocomplete
from django import forms

from blog.models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    """
    django-autocomplete-light 提供Form 层的组件来帮助我们更好的接入后端接口
    """
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
            'content', 'status'
        )