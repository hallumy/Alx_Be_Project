from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    
    filter_horizontal = ("trips",)

    def save_model(self, request, obj, form, change):
        
        super().save_model(request, obj, form, change)

        if "trips" in form.cleaned_data:
            obj.trips.set(form.cleaned_data["trips"])
            form.save_m2m()
            obj.calculate_totals()
            obj.save()

