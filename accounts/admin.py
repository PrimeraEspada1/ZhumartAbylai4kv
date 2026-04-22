from django.contrib import admin

from .models import Profile, ServiceRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", "user__email")


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "customer_name", "device_type", "status", "estimated_price", "created_at")
    list_filter = ("device_type", "status", "created_at")
    search_fields = ("title", "customer_name", "problem_description")
