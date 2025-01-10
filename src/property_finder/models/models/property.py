from django.db import models

from src.property_finder.models.models.agent import Agent


class PropertyTypeDepth(models.IntegerChoices):
    TYPE = 1
    SUB_TYPE = 2


class PropertyType(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    depth = models.IntegerField(choices=PropertyTypeDepth.choices, default=PropertyTypeDepth.TYPE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="sub_types")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Property type"
        verbose_name_plural = "Property types"


class Property(models.Model):
    main_type = models.ForeignKey(PropertyType, null=False, on_delete=models.PROTECT, related_name="main_type")
    sub_type = models.ForeignKey(PropertyType, null=False, blank=False, on_delete=models.PROTECT, related_name="sub_type")
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=False, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
