from django.contrib import admin

from main.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    """Payment model admin"""
    search_fields = ("name", "email", "address")
    list_display = ("__str__", "name", "created_at", "address")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Payment, PaymentAdmin)
