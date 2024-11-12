from django.contrib import admin
from app.models import *
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
   list_display = ('full_name', 'user', 'address', 'joined_on')


class ReviewAdmin(admin.ModelAdmin):
   list_display = ('id', 'user', 'product','rate', 'created_at')
admin.site.register(Admin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)




