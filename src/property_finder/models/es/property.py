from elasticsearch_dsl import Document, Keyword, Text


class PropertyDocument(Document):
    main_type = Text()
    sub_type = Text()
    title = Text()
    description = Text()
    agent_name = Keyword()

    class Index:
        name = 'properties'
