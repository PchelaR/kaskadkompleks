from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE

from .models import HeroBanner, Button, Post, PostImage, Service, About


class ButtonInline(admin.TabularInline):
    model = Button
    extra = 1
    max_num = 1


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']
    inlines = [ButtonInline]

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            HeroBanner.objects.filter(is_active=True).exclude(id=obj.id).update(is_active=False)

        super().save_model(request, obj, form, change)


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'text': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3
    max_num = 3


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'created_at']
    readonly_fields = ['slug', ]
    inlines = [PostImageInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    readonly_fields = ['slug', ]


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['custom_display_text']

    def custom_display_text(self, obj):
        return "Страница о компании"

    custom_display_text.short_description = 'Название страницы'

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True
