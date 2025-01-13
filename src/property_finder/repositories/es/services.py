from typing import Any, Dict, List, Tuple

from src.property_finder.models.types.types import ElasticsearchDocumentType


def document_update(
        document: ElasticsearchDocumentType,
        fields: List[str],
        data: Dict[str, Any]) -> Tuple[ElasticsearchDocumentType, bool]:
    """
    Generic update service meant to be reused in local update repositories for Elasticsearch.
    For example:
    def user_update(*, user: User, data) -> User:
        fields = ['first_name', 'last_name']
        user, has_updated = model_update(document=user, fields=fields, data=data)
        // Do other actions with the user here
        return user
    Return value: Tuple with the following elements:
        1. The document we updated
        2. A boolean value representing whether we performed an update or not.
    """
    has_updated = False
    for field in fields:
        # Skip if a field is not present in the actual data
        if field not in data:
            continue
        if getattr(document, field) != data[field]:
            has_updated = True
            setattr(document, field, data[field])
    # Perform an update only if any of the fields was actually changed
    if has_updated:
        document.save()
    return document, has_updated
