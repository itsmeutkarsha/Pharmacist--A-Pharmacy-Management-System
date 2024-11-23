# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaleItem, Medicine  # Make sure to import your models

@receiver(post_save, sender=SaleItem)
def update_medicine_stock(sender, instance, **kwargs):
    # Get the medicine and sale quantity from the SaleItem instance
    medicine = instance.medicine
    sale_quantity = instance.quantity

    # Ensure there's enough stock, then reduce it by the sale quantity
    if medicine.quantity_in_stock >= sale_quantity:
        medicine.quantity_in_stock -= sale_quantity
        medicine.save()
    else:
        # Handle the case where there's not enough stock
        raise ValueError("Not enough stock for this sale item.")



