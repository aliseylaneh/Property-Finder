from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from property_finder.models import Agent, Property, PropertyType


@registry.register_document
class PropertyDocument(Document):
    main_type = fields.ObjectField(properties={
        'title': fields.TextField()
    })
    sub_type = fields.ObjectField(properties={
        'title': fields.TextField()
    })
    agent = fields.ObjectField(properties={
        'name': fields.TextField()
    })

    class Index:
        name = 'properties'
        SETTINGS = {
            "number_of_shards": 3,  # Adjust based on the number of documents and hardware
            "number_of_replicas": 1,  # To ensure high availability
            "analysis": {
                "filter": {
                    "property_synonym_filter": {
                        "type": "synonym",
                        "synonyms": [
                            "apartment, flat",
                            "house, home",
                            "condo, condominium"
                        ]
                    },
                    "property_stop_filter": {
                        "type": "stop",
                        "stopwords": ["a", "an", "the", "for", "of", "and"]  # Add more based on your language context
                    }
                },
                "analyzer": {
                    "property_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "property_synonym_filter", "property_stop_filter"]
                    }
                }
            }
        }

    class Django:
        model = Property
        fields = ['title', 'description']
        related_models = [PropertyType, Agent]

    def get_queryset(self):
        queryset = super(PropertyDocument, self).get_queryset().select_related('main_type', 'sub_type', 'agent')
        return queryset
