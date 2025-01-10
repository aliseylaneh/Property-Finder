from elasticsearch_dsl import AsyncDocument, Keyword, Text


class PropertyDocument(AsyncDocument):
    main_type = Text()
    sub_type = Text()
    title = Text()
    description = Text()
    agent_name = Keyword()

    class Index:
        name = 'properties'
