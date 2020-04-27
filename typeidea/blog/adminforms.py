from dal import autocomplete
from django import forms

from blog.models import Category, Tag, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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

    content = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=True)
    # content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
    # content = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
            'content', 'status'
        )