import os
import io
import logging
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
from tinymce.models import HTMLField
from slugify import slugify

logger = logging.getLogger(__name__)


def convert_image_to_webp(image_file, quality=80):
    """
    Конвертирует изображение в формат WebP, снижает качество изображения до 80%.
    """
    try:
        image = Image.open(image_file)
        output = io.BytesIO()
        image.save(output, format='WEBP', quality=quality)
        output.seek(0)

        webp_name = os.path.splitext(image_file.name)[0] + '.webp'
        return ContentFile(output.read(), name=webp_name)
    except Exception as e:
        logger.error(f"Error converting image to WebP: {e}")
        return image_file


class HeroBanner(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero/', blank=False)
    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith('.webp'):
            self.image = convert_image_to_webp(self.image)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Button(models.Model):
    LINKS = (
        ('news', 'Новости'),
        ('articles', 'Статьи'),
        ('services', 'Услуги'),
        ('contacts', 'Контакты'),
    )

    title = models.CharField(max_length=20, blank=False)
    link = models.CharField(max_length=10, choices=LINKS)
    hero_banner = models.ForeignKey(HeroBanner, related_name='buttons', on_delete=models.CASCADE)


class Post(models.Model):
    TYPES = (
        ('New', 'Новость'),
        ('Article', 'Статья'),
    )

    title = models.CharField(max_length=60, blank=False, unique=True)
    type = models.CharField(max_length=10, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    text = HTMLField(blank=False)
    slug = models.SlugField(null=True, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith('.webp'):
            self.image = convert_image_to_webp(self.image)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.post.title}"


class Service(models.Model):
    title = models.CharField(max_length=255, blank=False, unique=True)
    text = HTMLField(blank=False)
    slug = models.SlugField(null=True, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class About(models.Model):
    text = HTMLField(blank=False)