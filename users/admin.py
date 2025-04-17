from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, OTP, BlacklistedAccessToken

# Custom UserAdmin adapted for a user model that uses phone_number without groups/user_permissions.
class UserAdmin(BaseUserAdmin):
    ordering = ('phone_number',)
    list_display = ('phone_number', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone_number',)
    # Override list_filter to exclude fields that don't exist on your user model.
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    # Override filter_horizontal to be empty because your model doesn't have these fields.
    filter_horizontal = ()

    # Fieldsets for displaying user details.
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    
    # Fieldsets for adding a new user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

# Register the custom user model
admin.site.register(User, UserAdmin)

# Simple OTP Admin
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('phone_number', 'code')

# BlacklistedAccessToken Admin
@admin.register(BlacklistedAccessToken)
class BlacklistedAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('jti', 'blacklisted_at')
    search_fields = ('jti',)


# cc96d54369e9480c97bd2722501e4af2