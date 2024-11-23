from django.urls import path
from . import views
from .views import (
    CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,
    SaleItemListView, SaleItemCreateView, SaleItemUpdateView, SaleItemDeleteView,
    SalesListView, SalesCreateView, SalesUpdateView, SalesDeleteView,
    SalesLogListView, SalesLogCreateView, SalesLogUpdateView, SalesLogDeleteView,
)

from .views import (
    MedicineListView, MedicineCreateView, MedicineUpdateView, MedicineDeleteView,
    PrescriptionListView, PrescriptionCreateView, PrescriptionUpdateView, PrescriptionDeleteView,
    PrescriptionItemListView, PrescriptionItemCreateView, PrescriptionItemUpdateView, PrescriptionItemDeleteView
)

from .views import (
    SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView,
    OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView,
    OrderItemListView, OrderItemCreateView, OrderItemUpdateView, OrderItemDeleteView,
    PrescriptionListView, PrescriptionCreateView, PrescriptionUpdateView, PrescriptionDeleteView,
    PrescriptionItemListView, PrescriptionItemCreateView, PrescriptionItemUpdateView, PrescriptionItemDeleteView,
    RoleListView, RoleCreateView, RoleUpdateView, RoleDeleteView,
    StaffListView,StaffCreateView,StaffUpdateView,StaffDeleteView,
    InventoryLogListView, InventoryLogCreateView, InventoryLogUpdateView, InventoryLogDeleteView
)

urlpatterns = [
    path('', views.home, name='core-home'),  # Route for the home page
    path('about/', views.about, name='core-about'),
    path('services/', views.services, name='core-services'),
    path('login/', views.login_view, name='core-login'),
    path('logout/', views.logout_view, name='core-logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Customer URLs
    path('customers/', CustomerListView.as_view(), name='customer_list'),        # Lists all customers
    path('customers/new/', CustomerCreateView.as_view(), name='customer_create'), # Creates a new customer
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_update'), # Edits a specific customer
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'), # Deletes a specific customer
    # path('customers/delete/<int:pk>/', CustomerDeleteView.as_view(), name='customer_delete'),

    # SaleItem URLs
    path('sale_items/', SaleItemListView.as_view(), name='saleitem_list'),
    path('sale_items/new/', SaleItemCreateView.as_view(), name='saleitem_create'),
    path('sale_items/<int:pk>/edit/', SaleItemUpdateView.as_view(), name='saleitem_update'),
    path('sale_items/<int:pk>/delete/', SaleItemDeleteView.as_view(), name='saleitem_delete'),

    # Sales URLs
    path('sales/', SalesListView.as_view(), name='sale_list'),
    path('sale/new/', SalesCreateView.as_view(), name='sale_create'),
    path('sale/<int:pk>/edit/', SalesUpdateView.as_view(), name='sale_update'),
    path('sale/<int:pk>/delete/', SalesDeleteView.as_view(), name='sale_delete'),

    # SalesLog URLs
    path('saleslogs/', SalesLogListView.as_view(), name='saleslog_list'),
    path('saleslogs/new/', SalesLogCreateView.as_view(), name='saleslog_create'),
    path('saleslogs/<int:pk>/edit/', SalesLogUpdateView.as_view(), name='saleslog_update'),
    path('saleslogs/<int:pk>/delete/', SalesLogDeleteView.as_view(), name='saleslog_delete'),

     # Medicine URLs
    path('medicines/', MedicineListView.as_view(), name='medicine_list'),
    path('medicines/add/', MedicineCreateView.as_view(), name='medicine_create'),
    path('medicines/<int:pk>/edit/', MedicineUpdateView.as_view(), name='medicine_update'),
    path('medicines/<int:pk>/delete/', MedicineDeleteView.as_view(), name='medicine_delete'),

    # Prescription URLs
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/add/', PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/<int:pk>/edit/', PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/<int:pk>/delete/', PrescriptionDeleteView.as_view(), name='prescription_delete'),

    # PrescriptionItem URLs
    path('prescription-items/', PrescriptionItemListView.as_view(), name='prescriptionitem_list'),
    path('prescription-items/add/', PrescriptionItemCreateView.as_view(), name='prescriptionitem_create'),
    path('prescription-items/<int:pk>/edit/', PrescriptionItemUpdateView.as_view(), name='prescriptionitem_update'),
    path('prescription-items/<int:pk>/delete/', PrescriptionItemDeleteView.as_view(), name='prescriptionitem_delete'),

     # Supplier URLs
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/update/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/delete/<int:pk>/', SupplierDeleteView.as_view(), name='supplier_delete'),

    # Order URLs
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),

    # Order Item URLs
    path('orderitems/', OrderItemListView.as_view(), name='orderitem_list'),
    path('orderitems/create/', OrderItemCreateView.as_view(), name='orderitem_create'),
    path('orderitems/update/<int:pk>/', OrderItemUpdateView.as_view(), name='orderitem_update'),
    path('orderitems/delete/<int:pk>/', OrderItemDeleteView.as_view(), name='orderitem_delete'),

    # Prescription URLs
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/create/', PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/update/<int:pk>/', PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/delete/<int:pk>/', PrescriptionDeleteView.as_view(), name='prescription_delete'),

    # Prescription Item URLs
    path('prescriptionitems/', PrescriptionItemListView.as_view(), name='prescriptionitem_list'),
    path('prescriptionitems/create/', PrescriptionItemCreateView.as_view(), name='prescriptionitem_create'),
    path('prescriptionitems/update/<int:pk>/', PrescriptionItemUpdateView.as_view(), name='prescriptionitem_update'),
    path('prescriptionitems/delete/<int:pk>/', PrescriptionItemDeleteView.as_view(), name='prescriptionitem_delete'),

    # Role URLs
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('roles/create/', RoleCreateView.as_view(), name='role_create'),
    path('roles/update/<int:pk>/', RoleUpdateView.as_view(), name='role_update'),
    path('roles/delete/<int:pk>/', RoleDeleteView.as_view(), name='role_delete'),

    # Staff URLs
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/create/', StaffCreateView.as_view(), name='staff_create'),
    path('staff/update/<int:pk>/', StaffUpdateView.as_view(), name='staff_update'),
    path('staff/delete/<int:pk>/', StaffDeleteView.as_view(), name='staff_delete'),

   # Inventory Log URLs
    path('inventorylogs/', InventoryLogListView.as_view(), name='inventorylog_list'),
    path('inventorylogs/create/', InventoryLogCreateView.as_view(), name='inventorylog_create'),
    path('inventorylogs/update/<int:pk>/', InventoryLogUpdateView.as_view(), name='inventorylog_update'),
    path('inventorylogs/delete/<int:pk>/', InventoryLogDeleteView.as_view(), name='inventorylog_delete'),

]

