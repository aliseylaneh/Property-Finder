from typing import TypeVar

from elasticsearch_dsl import Document

RepositoryModelType = TypeVar('RepositoryModelType', bound=str)
ElasticsearchDocumentType = TypeVar('ElasticsearchDocumentType', bound=Document)
