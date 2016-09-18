from django.contrib import admin
from .models import Client, SmsFac
from referral_system.models import  Appointment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django import forms

from models import AuthUser

from django.contrib.auth.forms import UserChangeForm
from django.forms import ChoiceField

def _remove_default_name_fields():
    user_display_fields =  list(UserAdmin.list_display)
    user_display_fields.remove('first_name')
    user_display_fields.remove('last_name')
    return tuple(user_display_fields)


class MsicUserChangeForm(UserChangeForm):
    facility_id = ChoiceField(label="Facility ID")
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    def __init__(self, *args, **kwargs):
        super(MsicUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['facility_id'] = ChoiceField(label="Facility ID")
        if self.instance:
            self.facility_id_field()
            self.fields['password'].widget.attrs['readonly'] = 'readonly'
            self.fields['first_name'].label = "Name"


    def clean_group(self):
        self.instance.groups.clear()
        self.instance.groups.add(self.cleaned_data['group'])
        return self.cleaned_data['group']

    class Meta:
        model = AuthUser
        fields = "__all__"

    class Media:
        js = ('referral_system/foundation-6.2.3/js/vendor/jquery.js', 'user_form.js')

    def facility_id_field(self):
        choices = [('', '-- Select --')]
        try:
            facilities = [(facility.quest_20, facility.quest_19) for facility in SmsFac.objects.all()]
            choices.extend(facilities)
            group = self.instance.groups.all()[0]
            self.fields['group'].initial = group
        except:
            pass
        self.fields['facility_id'] = ChoiceField(label="Facility ID", choices=choices, initial=self.instance.facility_id)




class MsicUserAdmin(UserAdmin):
    list_filter = ('groups__name',)
    UserAdmin.fieldsets = (
        ('Account credentials', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('User Type', {'fields': ('group', 'facility_id')}),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_display = _remove_default_name_fields() + ('name','user_type',)
    form = MsicUserChangeForm

    def name(self, obj):
        return obj.first_name

    def user_type(self, obj):
        try:
            return obj.groups.all()[0].name
        except Exception as e:
            return ''

    def facility_name(self, obj):
        return SmsFac.objects.get(quest_20=obj.facility_id).quest_19

    def save_model(self, request, obj, form, change):
        super(MsicUserAdmin, self).save_model(request, obj, form, change)



admin.site.unregister(Group)
#admin.site.unregister(User)

admin.site.register(AuthUser, MsicUserAdmin)

#admin.site.register(Client)
admin.site.register(SmsFac)
#admin.site.register(Appointment)
