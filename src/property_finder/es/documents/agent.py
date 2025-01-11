from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from property_finder.models import Agent


@registry.register_document
class AgentDocument(Document):
    class Index:
        name = 'agents'

    class Django:
        model = Agent
        fields = [
            'id',
            'name',
        ]
