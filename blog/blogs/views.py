from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BlogPostForm, UserRegistrationForm
from .models import BlogPost, Tag


def search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    
    posts = BlogPost.objects.filter(
        models.Q(title__icontains=query) | 
        models.Q(text__icontains=query) | 
        models.Q(summary__icontains=query)
    ).select_related('owner')[:5]  # Limit to 5 results for quick search
    
    results = []
    for post in posts:
        results.append({
            'title': post.title,
            'url': reverse('blogs:post_detail', args=[post.slug]),
            'excerpt': (post.summary or post.text)[:100] + '...',
            'date': post.date_added.strftime('%Y-%m-%d')
        })
    
    return JsonResponse({'results': results})


def index(request):
    tag_slug = request.GET.get('tag')
    query = request.GET.get('q', '').strip()
    posts = BlogPost.objects.select_related('owner').prefetch_related('tags')
    active_tag = None

    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    if query:
        posts = posts.filter(models.Q(title__icontains=query) | models.Q(text__icontains=query) | models.Q(summary__icontains=query))

    tags = Tag.objects.annotate(cnt=models.Count('posts')).filter(cnt__gt=0)
    hero_posts = posts.exclude(cover_url='').order_by('-date_added')[:5]
    total_posts = BlogPost.objects.count()
    total_tags = Tag.objects.count()
    latest_post = BlogPost.objects.order_by('-date_added').first()
    latest_posts = BlogPost.objects.order_by('-date_added')[:6]
    post_dates = [dt.date().isoformat() for dt in BlogPost.objects.values_list('date_added', flat=True)]
    return render(request, 'blogs/index.html', {
        'posts': posts,
        'tags': tags,
        'active_tag': active_tag,
        'query': query,
        'hero_posts': hero_posts,
        'total_posts': total_posts,
        'total_tags': total_tags,
        'latest_post': latest_post,
        'latest_posts': latest_posts,
        'post_dates': post_dates,
    })


@login_required
def new_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save(owner=request.user)
            return redirect('blogs:index')
    else:
        form = BlogPostForm()

    return render(request, 'blogs/post_form.html', {
        'form': form,
        'heading': '写一篇新的日志',
        'submit_label': '发布',
    })


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        raise Http404("You can't edit someone else's post.")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blogs/post_form.html', {
        'form': form,
        'heading': '编辑日志',
        'submit_label': '保存修改',
    })


def post_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.select_related('owner').prefetch_related('tags'), slug=slug)
    return render(request, 'blogs/detail.html', {'post': post})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blogs:index')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
