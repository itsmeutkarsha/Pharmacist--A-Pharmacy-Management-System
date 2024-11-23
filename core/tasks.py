# core/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Medicine

@shared_task
def check_medicine_stock(medicine_id=None):
    if medicine_id:
        # Check specific medicine
        medicine = Medicine.objects.filter(id=medicine_id, quantity_in_stock__lt=10).first()
        if medicine:
            medicine_list = f"{medicine.name} (Quantity: {medicine.quantity_in_stock})"
            send_stock_alert(medicine_list)
    else:
        # Check all medicines if no specific ID is given
        low_stock_medicines = Medicine.objects.filter(quantity_in_stock__lt=10)
        if low_stock_medicines.exists():
            medicine_list = "\n".join([f"{medicine.name} (Quantity: {medicine.quantity_in_stock})" for medicine in low_stock_medicines])
            send_stock_alert(medicine_list)

def send_stock_alert(medicine_list):
    send_mail(
        'Medicine Stock Alert',
        f'The following medicines are low in stock:\n\n{medicine_list}',
        settings.DEFAULT_FROM_EMAIL,
        ['utkarsha.rkusnake.cse23@itbhu.ac.in'],  # Replace with the manager's email
    )