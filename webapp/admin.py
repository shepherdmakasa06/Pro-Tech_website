from django.contrib import admin
from .models import Customer, Receipt, ReceiptItem

admin.site.register(Customer)
admin.site.register(Receipt)
admin.site.register(ReceiptItem)

# Register your models here.
