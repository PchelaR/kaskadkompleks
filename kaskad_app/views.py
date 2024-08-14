import os
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView
from .models import HeroBanner, Post, Service, About
from .utils import get_recent_posts
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from dotenv import load_dotenv

load_dotenv()


class HomepageView(TemplateView):
    template_name = 'kaskad_app/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hero_banners = HeroBanner.objects.filter(is_active=True).prefetch_related('buttons')
        context['hero_banners'] = hero_banners
        context['posts'] = get_recent_posts()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'kaskad_app/post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_recent_posts()
        return context


class NewsView(ListView):
    model = Post
    template_name = 'kaskad_app/newspage.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(type='New').order_by('-created_at').prefetch_related('images')


class ArticlesView(ListView):
    model = Post
    template_name = 'kaskad_app/articlespage.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(type='Article').order_by('-created_at').prefetch_related('images')


class ServicesView(TemplateView):
    template_name = 'kaskad_app/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.all()
        context['services'] = services
        return context


class ServiceDetail(DetailView):
    model = Service
    template_name = 'kaskad_app/service_detail.html'
    context_object_name = 'service_detail'


class AboutDetailView(DetailView):
    model = About
    template_name = 'kaskad_app/about.html'
    context_object_name = 'about'

    def get_object(self, queryset=None):
        return About.objects.first()


class ContactsView(FormView):
    template_name = 'kaskad_app/contactspage.html'
    form_class = ContactForm
    success_url = '/contact/success/'

    def post(self, request, *args, **kwargs):
        if getattr(request, 'limited', False):
            return render(request, 'kaskad_app/contact_unsuccess.html')

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f'Контактное сообщение от {first_name} {last_name}'
            body = f'Имя: {first_name} {last_name}\nEmail: {email}\nСообщение:\n{message}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = os.getenv('DEFAULT_FROM_EMAIL')

            email_message = EmailMessage(subject, body, from_email, [to_email])
            email_message.send()

            return super().form_valid(form)
        except Exception:
            return render(self.request, 'kaskad_app/contact_unsuccess.html')

    def form_invalid(self, form):
        return self.render_to_response({
            'form': form,
            'error_message': "Пожалуйста, исправьте ошибки ниже."
        })


def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        news_results = list(Post.objects.filter(type='New', title__icontains=query).values('title', 'slug'))
        articles_results = list(Post.objects.filter(type='Article', title__icontains=query).values('title', 'slug'))

        return JsonResponse({
            'data': {
                'news': news_results,
                'articles': articles_results
            }
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


class PageNotFoundView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'kaskad_app/404.html', status=404)
