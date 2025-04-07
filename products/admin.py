import csv
from django.contrib import admin
from django.http import HttpResponse
from django import forms
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = 'product_code', 'name', 'origin', 'made_in', 'quantity'
    list_display_links = 'product_code', 'name'
    # readonly_fields = 'origin', 'made_in'
    search_fields = 'name', 'origin', 'made_in'
    list_per_page = 25

# admin.site.register(Product, ProductAdmin)


# Form for CSV upload
class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(label="Select a CSV file")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name', 'origin', 'made_in', 'quantity']  # Fields to display
    actions = ['download_selected_as_csv']  # Add download action
    change_list_template = 'admin/products/product_change_list.html'  # Custom template for upload button

    # Action to download selected products as CSV
    def download_selected_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        # Write header
        writer.writerow(['product_code', 'name', 'origin', 'made_in', 'quantity'])

        # Write data for selected products
        for product in queryset:
            writer.writerow([
                product.product_code,
                product.name,
                product.origin,
                product.made_in,
                product.quantity
            ])

        return response
    download_selected_as_csv.short_description = "Download selected products as CSV"

    # Handle CSV upload
    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and 'upload_csv' in request.POST:
            form = CsvUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                # Process each row in the CSV
                for row in reader:
                    Product.objects.update_or_create(
                        product_code=row['product_code'],
                        defaults={
                            'name': row['name'],
                            'origin': row['origin'],
                            'made_in': row['made_in'],
                            'quantity': int(row['quantity'])
                        }
                    )
                self.message_user(request, "CSV uploaded and products imported successfully.")
        else:
            form = CsvUploadForm()

        extra_context = extra_context or {}
        extra_context['csv_upload_form'] = form
        return super().changelist_view(request, extra_context=extra_context)