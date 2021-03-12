from django.contrib import admin

# Register your models here.
from .models import Product, Tags, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Tags)
admin.site.register(Category)
