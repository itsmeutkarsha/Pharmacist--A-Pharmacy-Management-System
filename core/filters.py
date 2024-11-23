# myapp/filters.py
import django_filters # type: ignore
from .models import Medicine, Customer, Sale, SaleItem, Supplier

class MedicineFilter(django_filters.FilterSet):
    class Meta:
        model = Medicine
        fields = {
            'name': ['icontains'],  
            'category': ['exact'],
            'manufacturer': ['icontains'],
                   # Partial match for name                # Price filters (greater or less than)
        }

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'first_name': ['icontains'],  # Partial match for first name
            'last_name': ['icontains'],  # Partial match for last name
            # 'phone_number': ['exact'],  # Exact match for phone number
            # 'email': ['exact'],  # Exact match for email
        }


class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = {
            'customer__first_name': ['icontains'],  # Filter by customer's first name
            # 'customer__last_name': ['icontains'],   # Filter by customer's last name
            # 'date': ['exact', 'year__exact'],  # Exact date match or by year
            # 'total_amount': ['gte', 'lte'],  # Greater than or less than filters
        }

class SaleItemFilter(django_filters.FilterSet):
    class Meta:
        model = SaleItem
        fields = {
            'sale_id__customer__first_name': ['icontains'],  # Filter by customer's first name in Sale
            'sale_id__customer__last_name': ['icontains'],   # Filter by customer's last name in Sale
            'medicine__name': ['icontains'],  # Filter by medicine name
            # 'quantity': ['gte', 'lte'],  # Greater than or less than filters for quantity
            # 'price': ['gte', 'lte'],  # Greater than or less than filters for price
        }


class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'name': ['icontains'],  # Partial match for name
        #     'contact_person': ['icontains'],
        #     'phone_number': ['exact'],  # Exact match for phone number
        #     'email': ['exact'],  # Exact match for email
         }

