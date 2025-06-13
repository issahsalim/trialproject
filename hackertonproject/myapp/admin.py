from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import * 

# Register your models here.
class UserAccountAdmin(UserAdmin):
    list_display=('username','first_name','last_name','Course','email','is_superuser' )  
    search_fields=('username','first_name','last_name') 
    
    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Personal Info',{'fields':('Course','first_name','last_name','email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),

    )


    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'email','Course', 'password1', 'password2', 'is_staff', 'is_active',),
    }),
)
    ordering=('username',) 


admin.site.register(USERACCOUNT,UserAccountAdmin)


admin.site.register(Place)
admin.site.register(SupportMember)
admin.site.register(Questions)




# class PlaceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'latitude', 'longitude')
#     prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Place, PlaceAdmin)

# admin.site.register(TeamMember)
