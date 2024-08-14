from .models import Post


def get_recent_posts():
    """ Получение случайных постов и статей """
    new_posts = Post.objects.filter(type='New').order_by('?').prefetch_related('images')[:4]
    articles = Post.objects.filter(type='Article').order_by('?').prefetch_related('images')[:4]
    return new_posts | articles
