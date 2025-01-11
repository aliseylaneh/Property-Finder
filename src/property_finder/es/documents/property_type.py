from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from config.settings.elasticsearch import property_settings
from property_finder.models import PropertyType


@registry.register_document
class PropertyTypeDocument(Document):
    title = fields.TextField(
        analyzer="property_analyzer",
        fields={
            'keyword': fields.KeywordField(),
        }
    )

    class Index:
        name = 'property_types'
        settings = property_settings

    class Django:
        model = PropertyType
        fields = ['id', ]
