from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(ProductPhoto)
admin.site.register(Customer)