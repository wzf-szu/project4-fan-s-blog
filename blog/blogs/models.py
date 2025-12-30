from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            # 允许中文等非 ASCII，并为空时回退为原名
            candidate = slugify(self.name, allow_unicode=True) or self.name
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    text = models.TextField()
    summary = models.TextField(blank=True)
    cover_url = models.URLField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True) or self.title or f'post-{self.pk or "new"}'
            candidate = base
            idx = 1
            while BlogPost.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                idx += 1
                candidate = f"{base}-{idx}"
            self.slug = candidate
        super().save(*args, **kwargs)

    @property
    def word_count(self) -> int:
        return len(self.text.split()) if self.text else 0

    def __str__(self) -> str:
        return self.title
