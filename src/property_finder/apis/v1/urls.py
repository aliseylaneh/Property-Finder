from django.urls import include, path

from src.property_finder.apis.v1.propetry_types import GetAllPropertyTypeApi
from src.property_finder.apis.v1.agent import CreateAgentApi, DeleteAgentApi, SearchAgentApi, UpdateAgentApi
from src.property_finder.apis.v1.agent import GetAgentApi
from src.property_finder.apis.v1.property import CreatePropertyApi, DeletePropertyApi, GetPropertyApi, SearchPropertyApi, \
    UpdatePropertyApi

app_name = "v1"

urlpatterns = [
    # Property
    path('property/', include([
        path('create', CreatePropertyApi.as_view(), name='create-property'),
        path('<int:property_id>', GetPropertyApi.as_view(), name='get-property'),
        path('<int:property_id>/update', UpdatePropertyApi.as_view(), name='update-property'),
        path('<int:property_id>/delete', DeletePropertyApi.as_view(), name='delete-property'),
        path('search', SearchPropertyApi.as_view(), name='search-properties'),
    ])),
    path('agent/', include([
        path('<int:agent_id>', GetAgentApi.as_view(), name='get-agent'),
        path('create', CreateAgentApi.as_view(), name='create-agent'),
        path('<int:agent_id>/update', UpdateAgentApi.as_view(), name='update-agent'),
        path('<int:agent_id>/delete', DeleteAgentApi.as_view(), name='delete-agent'),
        path('search', SearchAgentApi.as_view(), name='search-agents'),

    ])),
    path('propertyTypes/', include([
        path('search', GetAllPropertyTypeApi.as_view(), name='search-property-types'),
    ]))
]
