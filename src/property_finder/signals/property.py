from django.db.models.signals import post_save
from django.dispatch import receiver

from src.property_finder.models import Agent
from src.property_finder.repositories.es.property_repo import PropertyElasticSearchRepository


@receiver(post_save, sender=Agent)
async def sync_property_to_elasticsearch(sender, instance, repository=PropertyElasticSearchRepository(), **kwargs):
    await repository.index(
        pk=instance.id,
        main_type_name=instance.main_type.title,
        sub_type_name=instance.sub_type.title,
        title=instance.title,
        description=instance.description,
        agent_name=instance.agent.name,
    )
