from django.contrib import admin
from core.models import Book, Category, CartOrder, CartOrderItem, Address


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "old_price", "get_percent_discount", "book_image", "in_stock", "is_new")
    list_filter = ["author", "category", "date_added"]
    search_fields = ["title", "author"]
    list_per_page = 10


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category_image"]


class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ["paid"]
    list_display = ["user", "total_amount", "paid", "order_date"]


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "invoice_number", "book", "quantity", "price", "total", "order_item_image"]


class AddressAdmin(admin.ModelAdmin):
    list_editable = ["status"]
    list_display = ["user", "address", "city", "state", "zipcode", "country", "phone", "status"]


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(Address, AddressAdmin)
