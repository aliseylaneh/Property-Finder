from elasticsearch_dsl import Document, Keyword, Text


class PropertyDocument(Document):
    type = Keyword()
    sub_type = Keyword()
    title = Text()
    description = Text()
    agent_id = Keyword()

    class Index:
        name = 'properties'
