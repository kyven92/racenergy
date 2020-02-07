from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from django import forms

from racIOT.models import *


class PlainUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ()
 

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ['first_name', 'last_name']
    list_display=['username','first_name','last_name','rps_id']

    fieldsets = UserAdmin.fieldsets+((None,{'fields':('rps_id',)}),)
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('rps_id', 'first_name', 'last_name','username','password'),
    }), )
    # form = UserChangeForm
    add_form = PlainUserForm


class RPS_Data_Admin(admin.ModelAdmin):
    list_display = [field.name for field in RPS_Data._meta.get_fields()]
    raw_id_fields = ['user_fk']



admin.site.register(User, CustomUserAdmin)
admin.site.register(RPS_Data,RPS_Data_Admin)
