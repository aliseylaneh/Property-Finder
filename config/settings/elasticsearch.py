from config.env_conf.env import env

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f'http://{env('ELASTICSEARCH_HOST')}:{env('ELASTICSEARCH_PORT')}',
    }
}
ELASTICSEARCH_DSL_AUTOSYNC = False  # Turned off this feature because we want to insert and sync manually

property_settings = {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
        "filter": {
            "property_synonym_filter": {
                "type": "synonym",
                "synonyms": [
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
                "filter": ["lowercase", "property_synonym_filter", "property_stop_filter"]
            }
        }
    }
}