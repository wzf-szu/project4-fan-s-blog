import os
import sys
import django

# Setup Django environment
# Assuming this script is in d:\pcc_3e-main\pcc_3e-main\chapter_19\blog\scripts
# We need to add d:\pcc_3e-main\pcc_3e-main\chapter_19\blog to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
blog_root = os.path.dirname(current_dir)
sys.path.append(blog_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')
django.setup()

from blogs.models import BlogPost, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

def run():
    # 1. Get a user
    user = User.objects.first()
    if not user:
        print("No user found. Creating a superuser 'admin'...")
        user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    
    print(f"Using user: {user.username}")

    # 2. Delete first 3 posts
    # We delete the 3 most recent posts to "refresh" the top of the blog
    posts_to_delete = BlogPost.objects.all().order_by('-date_added')[:3]
    count = posts_to_delete.count()
    
    if count > 0:
        print(f"Found {count} posts to delete.")
        # Convert to list to avoid issues when deleting while iterating querysets
        for post in list(posts_to_delete):
            print(f" - Deleting: {post.title}")
            post.delete()
    else:
        print("No posts found to delete.")

    # 3. Create new posts
    print("Creating new posts...")
    
    # Ensure tags exist
    tag_tech, _ = Tag.objects.get_or_create(name='Tech')
    tag_life, _ = Tag.objects.get_or_create(name='Life')
    tag_code, _ = Tag.objects.get_or_create(name='Coding')
    tag_mizuki, _ = Tag.objects.get_or_create(name='Mizuki')

    # Note: We use absolute URLs or placeholders that pass URLField validation if strict, 
    # but for local dev often relative paths work if not validated strictly on save.
    # However, to be safe and look good, let's use some placeholder images or assume static files exist.
    # The user has static files at /static/assets/desktop-banner/*.webp
    # We will use those.
    
    new_posts_data = [
        {
            "title": "Mizuki Theme Features Showcase",
            "summary": "A comprehensive guide to the features of the Mizuki theme, including dark mode, search, and responsive design.",
            "text": """# Welcome to Mizuki Theme

This is a demonstration of the **Mizuki** theme capabilities.

## Features

1. **Dark/Light Mode**: Toggle seamlessly between themes.
2. **Live Search**: Instant search results as you type.
3. **Responsive Design**: Looks great on mobile and desktop.

## Code Example

```python
def hello_mizuki():
    print("Hello, beautiful world!")
```

Enjoy your stay!""",
            "tags": [tag_tech, tag_mizuki],
            "cover_url": "/static/assets/desktop-banner/1.webp" 
        },
        {
            "title": "The Zen of Python",
            "summary": "Beautiful is better than ugly. Explicit is better than implicit.",
            "text": """# The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!""",
            "tags": [tag_code, tag_tech],
            "cover_url": "/static/assets/desktop-banner/2.webp"
        },
        {
            "title": "A Day in the Life",
            "summary": "Reflections on a peaceful day spent coding and enjoying coffee.",
            "text": """Today was a good day. I woke up early, brewed some fresh coffee, and sat down to write some code.

> "The best way to predict the future is to invent it." - Alan Kay

I worked on the **Mizuki Blog** project, refining the UI and adding new features. It's satisfying to see the pieces come together.

*   Coffee: Check
*   Code: Check
*   Music: Check

Time to relax now.""",
            "tags": [tag_life],
            "cover_url": "/static/assets/desktop-banner/3.webp"
        }
    ]

    for data in new_posts_data:
        # Bypass URL validation for relative paths by using update or just create if it doesn't complain
        # Django create() does not run full_clean()
        post = BlogPost.objects.create(
            title=data['title'],
            summary=data['summary'],
            text=data['text'],
            owner=user,
            cover_url=data['cover_url']
        )
        post.tags.set(data['tags'])
        print(f" + Created: {post.title}")

run()
