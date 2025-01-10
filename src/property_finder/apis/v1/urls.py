from django.urls import include, path

from src.property_finder.apis.v1.property import CreatePropertyApi

app_name = "v1"

urlpatterns = [
    # Property
    path('property/', include([
        path('create', CreatePropertyApi.as_view(), name='create-property'),
    ]))
]
