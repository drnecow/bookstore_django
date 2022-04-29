from django.contrib import admin
from storages.models import City, Storage, StorageEntry

# Register your models here.
admin.site.register(City)
admin.site.register(Storage)
admin.site.register(StorageEntry)