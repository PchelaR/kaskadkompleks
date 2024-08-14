from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import HomepageView, PostDetail, NewsView, ArticlesView, ServicesView, ServiceDetail, AboutDetailView, \
    ContactsView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('news/', NewsView.as_view(), name='news'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('services/', ServicesView.as_view(), name='services'),
    path('about/', AboutDetailView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contact'),
    path('search/', views.search_view, name='search'),
    path('contact/success/', TemplateView.as_view(template_name='kaskad_app/contact_success.html'),
         name='contact_success'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('services/<slug:slug>/', ServiceDetail.as_view(), name='service_detail'),
]
