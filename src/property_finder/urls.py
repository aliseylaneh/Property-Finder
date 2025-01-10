from django.urls import include, path

urlpatterns = [
    path("v1/", include("src.property_finder.apis.v1.urls", namespace='v1')),

]