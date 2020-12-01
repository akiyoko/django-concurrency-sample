from django.contrib import admin

from .models import Book, BookStock, Order


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)
    readonly_fields = ('id',)


class BookStockAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'updated_at', 'version')
    readonly_fields = ('id', 'updated_at', 'version')


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'ordered_by', 'ordered_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.ordered_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Book, BookAdmin)
admin.site.register(BookStock, BookStockAdmin)
admin.site.register(Order, OrderAdmin)
