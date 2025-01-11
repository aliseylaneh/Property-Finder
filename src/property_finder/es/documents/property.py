from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from config.settings.elasticsearch import property_settings
from src.property_finder.models import Agent, Property, PropertyType


@registry.register_document
class PropertyDocument(Document):
    main_type = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(
            analyzer="property_analyzer",
            fields={
                'keyword': fields.KeywordField(),
            }
        )
    })
    sub_type = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(
            analyzer="property_analyzer",
            fields={
                'keyword': fields.KeywordField(),
            }
        )
    })
    agent = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(
            analyzer="property_analyzer"
        )
    })
    title = fields.TextField(
        analyzer="property_analyzer",
        fields={
            'keyword': fields.KeywordField(),
        }
    )

    class Index:
        name = 'properties'
        settings = property_settings

    class Django:
        model = Property
        fields = ['description']
        related_models = [PropertyType, Agent]

    def get_queryset(self):
        queryset = super(PropertyDocument, self).get_queryset().select_related('main_type', 'sub_type', 'agent')
        return queryset
