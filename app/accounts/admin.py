
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import Company, Customer, Products, Credit, Debit,  Category, Expenses, UnitOfMeasurement, PaymentTypes, LoanAccounts, PurchaseOrderItem, PurchaseOrder

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)

admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(PaymentTypes)
admin.site.register(LoanAccounts)
admin.site.register(UnitOfMeasurement)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Expenses)
admin.site.register(Credit)
admin.site.register(Debit)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)




