from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from src.property_finder.models import Agent

agent_settings = {
    "number_of_shards": 1,  # Use 1 shard for smaller datasets to minimize overhead and latency.
    "number_of_replicas": 1,  # I only maintain 1 replica for availability.
    "analysis": {
        "filter": {
            "agent_synonym_filter": {
                "type": "synonym",
                "synonyms": [  # We can add more synonyms here for broadening search.
                    "realtor, broker",
                    "agent, representative",
                ]
            },
        },
        "tokenizer": {  # edge_ngram tokenizer will let us enable prefix matching on agent names
            "agent_edge_ngram_tokenizer": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 20,
                "token_chars": ["letter", "digit"]
            }
        },
        "analyzer": {
            "agent_analyzer": {
                "type": "custom",
                "tokenizer": "agent_edge_ngram_tokenizer",
                "filter": ["lowercase", "agent_synonym_filter"]  # Enabling case-insensitive
            }
        }
    }
}


@registry.register_document
class AgentDocument(Document):
    name = fields.TextField(
        analyzer="agent_analyzer",
        fields={
            'keyword': fields.KeywordField(),
        }
    )

    class Index:
        name = 'agents'
        settings = agent_settings

    class Django:
        model = Agent
        fields = [
            'id',
        ]
