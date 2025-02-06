from blog.models import Post, Tag
from django.db.models import Count
from django.shortcuts import get_object_or_404, render


def serialize_post(post):
    tags = post.tags.all()
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in tags],
        'first_tag_title': tags[0].title if tags else None,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_count if hasattr(tag, 'posts_count') else 0,
    }


def index(request):
    most_popular_posts = (
        Post.objects.popular()
        .select_related('author')
        .fetch_with_tags()
        .fetch_with_comments_count()[:5]
    )
    most_fresh_posts = (
        Post.objects.fetch_with_tags()
        .fetch_with_comments_count()[:5]
    )
    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = (
        get_object_or_404(Post.objects.prefetch_related(
            'author', 'likes', 'comments__author', 'tags')
            .annotate(likes_amount=Count('likes'))
            .filter(slug=slug))
    )
    serialized_comments = [
        {
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        } for comment in post.comments.all()
    ]
    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_amount,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
    }
    most_popular_tags = Tag.objects.popular()[:5]
    most_popular_posts = (
        Post.objects.popular()
        .fetch_with_tags()
        .fetch_with_comments_count()[:5]
    )
    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = (
        get_object_or_404(Tag.objects.prefetch_related(
            'posts__author', 'posts__tags')
            .filter(title=tag_title))
    )
    most_popular_tags = Tag.objects.popular()[:5]
    most_popular_posts = (
        Post.objects.popular()
        .prefetch_related('author')[:5]
        .fetch_with_comments_count()
    )
    related_posts = tag.posts.prefetch_related(
        'tags', 'author').fetch_with_comments_count()[:20]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
