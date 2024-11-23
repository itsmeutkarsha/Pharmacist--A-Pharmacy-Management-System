
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Pharmacy Schema


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)  # e.g., antibiotic, painkiller
    manufacturer = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=255)
    expiry_date = models.DateField()
    quantity_in_stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)
    date_issued = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"Prescription {self.prescription_id} for {self.customer}"


class PrescriptionItem(models.Model):
    prescription_item_id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.medicine} in Prescription {self.prescription}"


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.sale_id} by {self.customer}"


class SaleItem(models.Model):
    sale_item_id = models.AutoField(primary_key=True)
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.medicine} in Sale {self.sale}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_id} from {self.supplier}"


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.medicine} in Order {self.order}"


# User Management Schema

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name

# class Role(models.Model):
#     name = models.CharField(max_length=100)
#     group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="role", null=True, blank=True)  # Make it nullable

#     def __str__(self):
#         return self.name


# class Role(models.Model):
#     name = models.CharField(max_length=50)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name




class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# class Staff(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)

#     def assign_role_group(self):
#         # Get the group corresponding to this role
#         role_group, created = Group.objects.get_or_create(name=self.role.name)
        
#         # Add the group to the user, without clearing any existing groups
#         self.user.groups.add(role_group)
        
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.assign_role_group()



# Logs Schema

class InventoryLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # e.g., added, removed, updated
    quantity_changed = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.log_id} for {self.medicine} by {self.staff}"


class SalesLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)  # e.g., completed, refunded

    def __str__(self):
        return f"Sales Log {self.log_id} for Sale {self.sale}"



#Triggers
