from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False, )
    phone_number = models.CharField(max_length=50, null=False, blank=False, )

    def to_dict(self):
        return {"id": self.id, "name": self.name, }
