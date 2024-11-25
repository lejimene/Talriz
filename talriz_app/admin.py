from django.contrib import admin
from .models import  Item, ItemImage


#Testing like feature need admin not have like on its own device

class ItemAdmin(admin.ModelAdmin):
    exclude = ['likes']

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage)

# Register your models here.
