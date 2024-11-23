from django.contrib import admin
from .models import (
    Supplier,
    Customer,
    Medicine,
    Prescription,
    PrescriptionItem,
    Sale,
    SaleItem,
    Order,
    OrderItem,
    Role,
    Staff,
    InventoryLog,
    SalesLog
)

admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(InventoryLog)
admin.site.register(SalesLog)
