import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count

from .models import BlogPost, Tag


class BlogPostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='用逗号分隔标签，例如：Mizuki, Demo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '标签（可选）'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Prepopulate with existing tags for a smoother edit flow.
            self.fields['tags'].initial = ', '.join(self.instance.tags.values_list('name', flat=True))

    class Meta:
        model = BlogPost
        fields = ['title', 'summary', 'text', 'cover_url', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '标题'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '一句话摘要（可选）'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '正文'}),
            'cover_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': '封面图 URL（可选）'}),
        }

    def _sync_tags(self, instance, tags_raw: str):
        names = [t.strip() for t in tags_raw.split(',') if t.strip()]
        instance.tags.clear()
        for name in names:
            tag, _ = Tag.objects.get_or_create(name=name)
            instance.tags.add(tag)
        # 清理无关联的标签，避免侧栏残留
        Tag.objects.annotate(cnt=Count('posts')).filter(cnt=0).delete()

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        if not raw:
            return ''
        # 去除用户可能看到的 [] 或 [<Tag: ...>] 杂质文本
        cleaned = re.sub(r'\[|\]|<Tag:|>', '', str(raw))
        parts = [p.strip() for p in cleaned.split(',') if p.strip()]
        return ', '.join(parts)

    def save(self, commit=True, owner=None):
        instance = super().save(commit=False)
        if owner and not instance.owner_id:
            instance.owner = owner
        if commit:
            instance.save()
            self._sync_tags(instance, self.cleaned_data.get('tags', ''))
        else:
            self._pending_tags = self.cleaned_data.get('tags', '')
        return instance

    def save_m2m(self):
        super().save_m2m()
        if hasattr(self, '_pending_tags'):
            self._sync_tags(self.instance, self._pending_tags)


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
