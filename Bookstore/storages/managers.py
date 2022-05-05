from django.db import models


# Manager for Storage model
class StorageQuerySet(models.QuerySet):
    def all(self):
        return self

    def functional(self):
        return self.filter(is_functional=True)
