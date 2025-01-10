from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from src.property_finder.models.django.agent import Agent
from src.property_finder.repositories.es.agent_repo import AgentElasticSearchRepository


@receiver(post_save, sender=Agent)
def sync_agent_to_elasticsearch(sender,
                                instance,
                                created,
                                repository: AgentElasticSearchRepository = AgentElasticSearchRepository(),
                                **kwargs):
    if created:
        # Index new agent in Elasticsearch
        repository.index(
            pk=instance.id,
            name=instance.name,
            email=instance.email,
            phone_number=instance.phone_number
        )
    else:
        # Update existing agent in Elasticsearch
        repository.index(
            pk=instance.id,
            name=instance.name,
            email=instance.email,
            phone_number=instance.phone_number
        )


@receiver(post_delete, sender=Agent)
def delete_agent_from_elasticsearch(sender,
                                    instance: Agent,
                                    repository: AgentElasticSearchRepository = AgentElasticSearchRepository(),
                                    **kwargs):
    repository.delete(pk=str(instance.id))
