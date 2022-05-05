from django.db import models


# Manager for SupplyEntry model
class SupplyEntryQuerySet(models.QuerySet):
    def all(self):
        return self

    def waiting_for_delivery(self):
        return self.filter(status=1)

    def late(self):
        return self.filter(status=2)

    def delivered(self):
        return self.filter(status=3)

    def cancelled(self):
        return self.filter(status=4)
