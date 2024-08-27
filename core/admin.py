from django.contrib import admin
from core.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# admin.site.register(User, UserAdmin)

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass

class UserAdmin(BaseUserAdmin):
    # fieldsets = BaseUserAdmin.fieldsets[1:] + ((None, {"fields": ("email", "password")}),) 
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)