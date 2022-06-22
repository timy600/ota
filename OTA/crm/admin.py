from django.contrib import admin
from .models import User, Invoice

class InvoiceInline(admin.TabularInline):
    model = Invoice
    ordering = ["date"]
    readonly_fields = ["ref"]
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {'fields':["name", "email"]}
        ),
        (
            "Company References",
            {
                "fields": ["company", "country", "invoice_currency"],
                "classes":["collapse"]
            }
        )
    ]
    inlines = [InvoiceInline]

    def has_delete_permission(self, request, obj=None):
        # count_invoices = obj.invoices.count()
        # print(Invoice.objects.filter(user=))
        # if len(count_invoices) == 0:
        #     return True
        return False

#admin.site.register(User)
#admin.site.register(Invoice)
admin.site.register(User, UserAdmin)
