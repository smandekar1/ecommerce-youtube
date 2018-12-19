from django.contrib import admin

# Register your models here.
# from .models import Viewed_Product

# class Viewed_ProductAdmin(admin.ModelAdmin):
# 	list_display = ['__str__', 'slug']
# 	class Meta:
# 		model = Viewed_Product


# admin.site.register(Viewed_Product, Viewed_ProductAdmin)


from .models import Viewed_Product_User, Viewed_Product_Object

admin.site.register(Viewed_Product_User)
admin.site.register(Viewed_Product_Object)
