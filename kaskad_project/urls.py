from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from kaskad_app.views import PageNotFoundView

handler404 = PageNotFoundView.as_view()

urlpatterns = [
    path('superplot-dm/', admin.site.urls),
    path('', include('kaskad_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

