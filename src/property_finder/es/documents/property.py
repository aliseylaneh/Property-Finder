from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from src.property_finder.models import Agent, Property, PropertyType

property_settings = {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
        "filter": {
            "property_synonym_filter": {
                "type": "synonym",
                "synonyms": [  # We can add more synonyms here for broadening search.
                    "apartment, flat", "beds, bedrooms",
                    "house, home", "wc, toilet,shower",
                    "condo, condominium", "balcony, balconies"
                ]
            },
            "property_stop_filter": {
                "type": "stop",
                "stopwords": ["a", "an", "the", "for", "of", "and", ]
            }
        },
        "analyzer": {
            "property_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase", "property_synonym_filter", "property_stop_filter"]  # Enabling case-insensitive
            }
        }
    }
}


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
