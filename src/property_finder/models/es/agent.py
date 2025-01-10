from elasticsearch_dsl import AsyncDocument, Keyword, Text


class AgentDocument(AsyncDocument):
    name = Text()
    email = Keyword()
    phone_number = Keyword()

    class Index:
        name = 'agents'
