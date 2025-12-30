import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Blog.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from blogs.models import BlogPost  # noqa: E402

User = get_user_model()
user, _ = User.objects.get_or_create(username="demo")
user.set_password("demo1234")
user.save()

posts = [
    ("欢迎来到 Mizuki 博客", "这是示例帖，展示布局与主题。"),
    (
        "Markdown 与代码高亮",
        "支持基础 Markdown 渲染，尝试写一些代码片段：\n\n    print(\"hello mizuki\")",
    ),
    ("权限示例", "未登录只能查看，登录后才能新建或编辑属于自己的帖子。"),
]

for title, text in posts:
    BlogPost.objects.update_or_create(title=title, owner=user, defaults={"text": text})

print("demo user ready; posts:", BlogPost.objects.count())
