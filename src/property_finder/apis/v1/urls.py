from django.urls import include, path

from src.property_finder.apis.v1.agent import CreateAgentApi, DeleteAgentApi, SearchAgentApi, UpdateAgentApi
from src.property_finder.apis.v1.property import CreatePropertyApi

app_name = "v1"

urlpatterns = [
    # Property
    path('property/', include([
        path('create', CreatePropertyApi.as_view(), name='create-property'),
    ])),
    path('agent/', include([
        path('create', CreateAgentApi.as_view(), name='create-agent'),
        path('<int:agent_id>/update', UpdateAgentApi.as_view(), name='update-agent'),
        path('<int:agent_id>/delete', DeleteAgentApi.as_view(), name='delete-agent'),
        path('search', SearchAgentApi.as_view(), name='search-agents'),

    ]))
]
