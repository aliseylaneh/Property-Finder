from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
                  path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
                  path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
                  path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
                  path('api/', include(('src.property_finder.urls', 'property_finder'))),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
