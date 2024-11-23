from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Customer, SalesLog, Sale,SaleItem, Customer, Prescription, PrescriptionItem, Medicine, Supplier, Order, OrderItem, Role, Staff, InventoryLog
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from .filters import MedicineFilter,CustomerFilter,SaleFilter, SaleItemFilter, SupplierFilter




#temperorily bypass the csrf token part
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'core/home.html')

def services(request):
    return render(request, 'core/services.html')

def about(request):
    return render(request, 'core/about.html')

def logout_view(request):
    logout(request)
    return redirect("login")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'core/login.html')


    
@csrf_exempt
@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Pharmacist').exists():
        return render(request, 'core/Pharmacist_dashboard.html')
    elif user.groups.filter(name='Cashier').exists():
        return render(request, 'core/Cashier_dashboard.html')
    elif user.groups.filter(name='Manager').exists():
        return render(request, 'core/Manager_dashboard.html')
    elif user.groups.filter(name='Inventory manager').exists():
        return render(request, 'core/Inventory_manager_dashboard.html')
    else:
        # Redirect or show a page for users without specific roles
        return render(request, 'no_role_dashboard.html')


def is_cashier(user):
    return user.groups.filter(name='cashier').exists()

#the below line is added for temperory bypassing the csrf
@csrf_exempt
@login_required
@user_passes_test(is_cashier)
def cashier_dashboard(request):
    customers = Customer.objects.all()
    sales = Sale.objects.all()
    sale_items = SaleItem.objects.all()
    sales_logs = SalesLog.objects.all()

    context = {
        'customers': customers,
        'sales': sales,
        'sale_items': sale_items,
        'sales_logs': sales_logs
    }

    return render(request, 'cashier_dashboard.html', context)

def is_pharmacist(user):
    return user.groups.filter(name='Pharmacist').exists()

@csrf_exempt  # Temporary bypass for CSRF, use with caution
@login_required
@user_passes_test(is_pharmacist)
def pharmacist_dashboard(request):
    customers = Customer.objects.all()
    prescriptions = Prescription.objects.all()
    prescription_items = PrescriptionItem.objects.all()
    medicines = Medicine.objects.all()

    context = {
        'customers': customers,
        'prescriptions': prescriptions,
        'prescription_items': prescription_items,
        'medicines': medicines
    }

    return render(request, 'Pharmacist_dashboard.html', context)

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@csrf_exempt  # Temporary bypass for CSRF, use with caution
@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    # Retrieve all relevant data for the dashboard
    customers = Customer.objects.all()
    suppliers = Supplier.objects.all()
    medicines = Medicine.objects.all()
    prescriptions = Prescription.objects.all()
    prescription_items = PrescriptionItem.objects.all()
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()
    roles = Role.objects.all()
    staff = Staff.objects.all()
    sales = Sale.objects.all()  # Assuming Sale is the model for sales
    sale_items = SaleItem.objects.all()  # Assuming SaleItem is the model for sale items
    sales_logs = SalesLog.objects.all()  # Assuming SalesLog is the model for sales logs

    context = {
        'customers': customers,
        'suppliers': suppliers,
        'medicines': medicines,
        'prescriptions': prescriptions,
        'prescription_items': prescription_items,
        'orders': orders,
        'order_items': order_items,
        'roles': roles,
        'staff': staff,
        'sales': sales,
        'sale_items': sale_items,
        'sales_logs': sales_logs,
    }

    return render(request, 'core/Manager_dashboard.html', context)



# class CustomerListView(ListView):
#     model = Customer
#     template_name = "core/customer/list.html"  # Path to the organized template

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Pass fields to use in the template
#         context['fields'] = self.model._meta.fields
#         return context


class CustomerListView(ListView):
    model = Customer
    template_name = 'core/customer/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CustomerFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        context['filterset'] = self.filterset
        return context


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'address']
    template_name = 'core/customer/form.html'  # Updated path
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'address']
    template_name = 'core/customer/form.html'  # Updated path
    success_url = reverse_lazy('customer_list')

# class CustomerDeleteView(DeleteView):
#     model = Customer
#     template_name = 'core/customer/confirm_delete.html'  # Updated path
#     success_url = reverse_lazy('customer_list')


class CustomerDeleteView(DeleteView):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'core/customer/confirm_delete.html', {'customer': customer, 'cancel_url': 'customer_list'})  # Ensure the correct cancel URL

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return redirect('customer_list')  # Redirect after deletion
 
 #for sale items


# class SaleItemListView(ListView):
#     model = SaleItem
#     template_name = 'core/sale_items/list.html'  # Adjust to your path

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['fields'] = self.model._meta.fields  # Pass the fields to the template
#         return context


class SaleItemListView(ListView):
    model = SaleItem
    template_name = 'core/sale_items/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SaleItemFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['sale', 'medicine', 'quantity', 'price']
        context['filterset'] = self.filterset
        return context

class SaleItemCreateView(CreateView):
    model = SaleItem
    fields = ['sale_id','medicine', 'quantity', 'price']
    template_name = 'core/sale_items/form.html'  # Use sale_items folder and new form template
    success_url = reverse_lazy('saleitem_list')  # Redirect to list view after creation

class SaleItemUpdateView(UpdateView):
    model = SaleItem
    fields = ['medicine', 'quantity', 'price']
    template_name = 'core/sale_items/form.html'  # Reuse form template for both create and update
    success_url = reverse_lazy('saleitem_list')

# class SaleItemDeleteView(DeleteView):
#     model = SaleItem
#     template_name = 'core/sale_items/confirm_delete.html'  # Use sale_items folder and new delete template
#     success_url = reverse_lazy('saleitem_list')


class SaleItemDeleteView(DeleteView):
    def get(self, request, pk):
        sale_item = get_object_or_404(SaleItem, pk=pk)
        return render(request, 'core/sale_items/confirm_delete.html', {'sale_item': sale_item, 'cancel_url': 'saleitem_list'})  # Ensure correct cancel URL

    def post(self, request, pk):
        sale_item = get_object_or_404(SaleItem, pk=pk)
        sale_item.delete()
        return redirect('saleitem_list')  # Redirect to list view after deletion

#for sales


# class SalesListView(ListView):
#     model = Sale
#     template_name = 'core/sale/list.html'  # Adjust to your path

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['fields'] = self.model._meta.fields  # Pass the fields to the template
#         return context

class SalesListView(ListView):
    model = Sale
    template_name = 'core/sale/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SaleFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['customer', 'date', 'total_amount']
        context['filterset'] = self.filterset
        return context

class SalesCreateView(CreateView):
    model = Sale
    fields = ['customer', 'date', 'total_amount']
    template_name = 'core/sale/form.html'
    success_url = reverse_lazy('sale_list')

class SalesUpdateView(UpdateView):
    model = Sale
    fields = ['customer', 'date', 'total_amount']
    template_name = 'core/sale/form.html'
    success_url = reverse_lazy('sale_list')

# class SalesDeleteView(DeleteView):
#     model = Sale
#     template_name = 'core/sale/confirm_delete.html'
#     success_url = reverse_lazy('sale_list')


class SalesDeleteView(DeleteView):
    model = Sale
    template_name = 'core/sale/confirm_delete.html'
    success_url = reverse_lazy('sale_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('sale_list')  # Or another appropriate URL for this view
        return context


# class SaleDeleteView(DeleteView):
#     def get(self, request, pk):
#         sale = get_object_or_404(Sale, pk=pk)
#         return render(request, 'core/sale/confirm_delete.html', {'sale': sale, 'cancel_url': 'sale_list'})  # Ensure the correct cancel URL

#     def post(self, request, pk):
#         sale = get_object_or_404(Sale, pk=pk)
#         sale.delete()
#         return redirect('sale_list')  # Redirect to list view after deletion
    
#for saleslog
class SalesLogListView(ListView):
    model = SalesLog
    template_name = 'core/saleslog/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['sale', 'staff', 'action']  # List of fields to display in the template
        return context

class SalesLogCreateView(CreateView):
    model = SalesLog
    fields = ['sale', 'staff', 'action']
    template_name = 'core/saleslog/form.html'
    success_url = reverse_lazy('saleslog_list')

class SalesLogUpdateView(UpdateView):
    model = SalesLog
    fields = ['sale', 'staff', 'action']
    template_name = 'core/saleslog/form.html'
    success_url = reverse_lazy('saleslog_list')

class SalesLogDeleteView(DeleteView):
    model = SalesLog
    template_name = 'core/saleslog/confirm_delete.html'
    success_url = reverse_lazy('saleslog_list')


# Medicine Views
# class MedicineListView(ListView):
#     model = Medicine
#     template_name = 'core/medicine/list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['fields'] = ['name', 'category', 'manufacturer', 'batch_number', 'expiry_date', 'quantity_in_stock', 'price']
#         return context


class MedicineListView(ListView):
    model = Medicine
    template_name = 'core/medicine/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = MedicineFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['name', 'category', 'manufacturer', 'batch_number', 'expiry_date', 'quantity_in_stock', 'price']
        context['filterset'] = self.filterset  # Pass the filterset to the template
        return context
    

class MedicineCreateView(CreateView):
    model = Medicine
    fields = ['name', 'category', 'manufacturer', 'batch_number', 'expiry_date', 'quantity_in_stock', 'price']
    template_name = 'core/medicine/form.html'
    success_url = reverse_lazy('medicine_list')

class MedicineUpdateView(UpdateView):
    model = Medicine
    fields = ['name', 'category', 'manufacturer', 'batch_number', 'expiry_date', 'quantity_in_stock', 'price']
    template_name = 'core/medicine/form.html'
    success_url = reverse_lazy('medicine_list')

class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = 'core/medicine/confirm_delete.html'
    success_url = reverse_lazy('medicine_list')

# Prescription Views
class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'core/prescription/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['customer', 'doctor_name', 'date_issued', 'notes']
        return context

class PrescriptionCreateView(CreateView):
    model = Prescription
    fields = ['customer', 'doctor_name', 'date_issued', 'notes']
    template_name = 'core/prescription/form.html'
    success_url = reverse_lazy('prescription_list')

class PrescriptionUpdateView(UpdateView):
    model = Prescription
    fields = ['customer', 'doctor_name', 'date_issued', 'notes']
    template_name = 'core/prescription/form.html'
    success_url = reverse_lazy('prescription_list')

class PrescriptionDeleteView(DeleteView):
    model = Prescription
    template_name = 'core/prescription/confirm_delete.html'
    success_url = reverse_lazy('prescription_list')

# PrescriptionItem Views
class PrescriptionItemListView(ListView):
    model = PrescriptionItem
    template_name = 'core/prescriptionitem/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['prescription', 'medicine', 'dosage', 'quantity', 'price']
        return context

class PrescriptionItemCreateView(CreateView):
    model = PrescriptionItem
    fields = ['prescription', 'medicine', 'dosage', 'quantity', 'price']
    template_name = 'core/prescriptionitem/form.html'
    success_url = reverse_lazy('prescriptionitem_list')

class PrescriptionItemUpdateView(UpdateView):
    model = PrescriptionItem
    fields = ['prescription', 'medicine', 'dosage', 'quantity', 'price']
    template_name = 'core/prescriptionitem/form.html'
    success_url = reverse_lazy('prescriptionitem_list')

class PrescriptionItemDeleteView(DeleteView):
    model = PrescriptionItem
    template_name = 'core/prescriptionitem/confirm_delete.html'
    success_url = reverse_lazy('prescriptionitem_list')


# View for suppliers
# class SupplierListView(ListView):
#     model = Supplier
#     template_name = 'core/supplier/list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['fields'] = ['name', 'contact_person', 'phone_number', 'email', 'address']
#         return context


class SupplierListView(ListView):
    model = Supplier
    template_name = 'core/supplier/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SupplierFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['name', 'contact_person', 'email', 'phone_number', 'address']
        context['filterset'] = self.filterset
        return context

class SupplierCreateView(CreateView):
    model = Supplier
    fields = ['name', 'contact_person', 'phone_number', 'email', 'address']
    template_name = 'core/supplier/form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = ['name', 'contact_person', 'phone_number', 'email', 'address']
    template_name = 'core/supplier/form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'core/supplier/confirm_delete.html'
    success_url = reverse_lazy('supplier_list')


#view for orders
class OrderListView(ListView):
    model = Order
    template_name = 'core/order/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['supplier', 'order_date', 'total_cost']
        return context


class OrderCreateView(CreateView):
    model = Order
    fields = ['supplier', 'order_date', 'total_cost']
    template_name = 'core/order/form.html'
    success_url = reverse_lazy('order_list')

class OrderUpdateView(UpdateView):
    model = Order
    fields = ['supplier', 'order_date', 'total_cost']
    template_name = 'core/order/form.html'
    success_url = reverse_lazy('order_list')

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'core/order/confirm_delete.html'
    success_url = reverse_lazy('order_list')

# List View for OrderItem
class OrderItemListView(ListView):
    model = OrderItem
    template_name = 'core/orderitem/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['order', 'medicine', 'quantity', 'cost']
        return context


class OrderItemCreateView(CreateView):
    model = OrderItem
    fields = ['order', 'medicine', 'quantity', 'cost']
    template_name = 'core/orderitem/form.html'
    success_url = reverse_lazy('orderitem_list')

class OrderItemUpdateView(UpdateView):
    model = OrderItem
    fields = ['order', 'medicine', 'quantity', 'cost']
    template_name = 'core/orderitem/form.html'
    success_url = reverse_lazy('orderitem_list')

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = 'core/orderitem/confirm_delete.html'
    success_url = reverse_lazy('orderitem_list')


#View for Role
class RoleListView(ListView):
    model = Role
    template_name = 'core/role/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['role_name']
        return context



class RoleCreateView(CreateView):
    model = Role
    fields = ['role_name']
    template_name = 'core/role/form.html'
    success_url = reverse_lazy('role_list')


class RoleUpdateView(UpdateView):
    model = Role
    fields = ['role_name']
    template_name = 'core/role/form.html'
    success_url = reverse_lazy('role_list')

class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'core/role/confirm_delete.html'
    success_url = reverse_lazy('role_list')

#View for Staff
class StaffListView(ListView):
    model = Staff
    template_name = 'core/staff/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['first_name', 'last_name', 'role', 'username', 'email', 'phone_number']
        return context



class StaffCreateView(CreateView):
    model = Staff
    fields = ['first_name', 'last_name', 'role', 'username', 'password', 'email', 'phone_number']
    template_name = 'core/staff/form.html'
    success_url = reverse_lazy('staff_list')


class StaffUpdateView(UpdateView):
    model = Staff
    fields = ['first_name', 'last_name', 'role', 'username', 'password', 'email', 'phone_number']
    template_name = 'core/staff/form.html'
    success_url = reverse_lazy('staff_list')


class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'core/staff/confirm_delete.html'
    success_url = reverse_lazy('staff_list')

# View for InventoryLog
class InventoryLogListView(ListView):
    model = InventoryLog
    template_name = 'core/inventorylog/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['medicine', 'staff', 'action', 'quantity_changed', 'date']
        return context

class InventoryLogCreateView(CreateView):
    model = InventoryLog
    fields = ['medicine', 'staff', 'action', 'quantity_changed']
    template_name = 'core/inventorylog/form.html'
    success_url = reverse_lazy('inventorylog_list')

class InventoryLogUpdateView(UpdateView):
    model = InventoryLog
    fields = ['medicine', 'staff', 'action', 'quantity_changed']
    template_name = 'core/inventorylog/form.html'
    success_url = reverse_lazy('inventorylog_list')

class InventoryLogDeleteView(DeleteView):
    model = InventoryLog
    template_name = 'core/inventorylog/confirm_delete.html'
    success_url = reverse_lazy('inventorylog_list')
