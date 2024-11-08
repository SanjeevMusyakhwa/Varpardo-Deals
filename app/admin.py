from django.contrib import admin
from app.models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Cart)

