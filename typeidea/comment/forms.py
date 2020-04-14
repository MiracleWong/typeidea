from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, label='昵称', widget=forms.widgets.Input(
        attrs={
            'class': 'form-control',
            'style': 'width: 60%;'
        }
    ))
    email = forms.CharField(max_length=50, label='Email', widget=forms.widgets.EmailInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 60%;'
        }
    ))
    website = forms.CharField(max_length=100, label='网站', widget=forms.widgets.URLInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 60%;'
        }
    ))
    content = forms.CharField(max_length=500, label='内容', widget=forms.widgets.Textarea(
        attrs={
            'rows': 6,
            'cols': 60,
            'class': 'form-control'
        }
    ))

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容怎么这么短呢，需要大于10个字哟')

        return content

    class Meta:
        model = Comment
        fields= ['nickname', 'email', 'website', 'content']