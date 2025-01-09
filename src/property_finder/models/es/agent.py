from elasticsearch_dsl import Document, Keyword, Text


class AgentDocument(Document):
    name = Text()
    email = Keyword()
    phone_number = Keyword()

    class Index:
        name = 'agents'
