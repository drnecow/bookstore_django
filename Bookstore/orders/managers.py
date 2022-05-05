from django.db import models


# Manager for OrderEntry model
class OrderEntryQuerySet(models.QuerySet):
    def all(self):
        return self

    def in_assembly(self):
        return self.filter(status=1)

    def waiting_for_payment(self):
        return self.filter(status=2)

    def waiting_for_delivery(self):
        return self.filter(status=3)

    def late(self):
        return self.filter(status=4)

    def delivered(self):
        return self.filter(status=5)

    def cancelled(self):
        return self.filter(status=6)
