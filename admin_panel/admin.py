from django.contrib import admin
from .models import ReportedUser, ReportedProduct


@admin.register(ReportedUser)
class ReportedUserAdmin(admin.ModelAdmin):
    list_display = ('reported_user', 'reporter', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reported_user__username', 'reporter__username', 'reason')
    readonly_fields = ('created_at',)


@admin.register(ReportedProduct)
class ReportedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'reporter', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product__name', 'reporter__username', 'reason')
    readonly_fields = ('created_at',)
