from django.contrib import admin

from src.property_finder.models import Agent, Property, PropertyType


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    pass


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    pass
