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


def get_facility_choices():
    choices_facility = [('', '-- Select --')]
    facility_objects = SmsFac.objects.filter(quest_50__in=["Both (Referral System and Public Facing Platform)",
                                                           "Referral System only"]).order_by('quest_19')
    facilities = [(facility.quest_20, facility.quest_19) for facility in facility_objects]
    choices_facility.extend(facilities)
    return choices_facility

def get_garment_choices():
    choices_garment = [('', '-- Select --')]
    garments = [(facility.quest_20, facility.quest_19) for facility in
                                                       SmsFac.objects.filter(quest_21="Garment factory infirmary").
                                                       order_by('quest_19')]
    choices_garment.extend(garments)
    return choices_garment


class MsicUserChangeForm(UserChangeForm):
    facility_id = ChoiceField(label="Facility", choices=get_facility_choices, required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)
    garment_id = ChoiceField(label="Garment", choices=get_garment_choices, required=False)

    def __init__(self, *args, **kwargs):
        super(MsicUserChangeForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.facility_id_field()
            self.fields['password'].widget.attrs['readonly'] = 'readonly'
            self.fields['first_name'].label = "Name"


    def clean_group(self):
        self.instance.groups.clear()
        self.instance.groups.add(self.cleaned_data['group'])
        if self.cleaned_data['group'] == '3':
            self.instance.facility_id = self.cleaned_data['facility_id']
        elif self.cleaned_data['group'] == '2':
            self.instance.facility_id = self.cleaned_data['garment_id']
        return self.cleaned_data['group']

    class Meta:
        model = AuthUser
        fields = "__all__"

    class Media:
        js = ('referral_system/foundation-6.2.3/js/vendor/jquery.js', 'user_form.js')

    def facility_id_field(self):
        try:
            group = self.instance.groups.all()[0]
            self.fields['group'].initial = group
            self.fields['facility_id'].initial = self.instance.facility_id
            self.fields['garment_id'].initial = self.instance.facility_id
        except Exception as e:
            pass
        


class MsicUserAdmin(UserAdmin):
    list_filter = ('groups__name',)
    UserAdmin.fieldsets = (
        ('Account credentials', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('User Type', {'fields': ('group', 'facility_id', 'garment_id')}),
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
        if obj.groups.all()[0].name == "Garment Factory":
            obj.facility_id = form.cleaned_data['garment_id']
        super(MsicUserAdmin, self).save_model(request, obj, form, change)



admin.site.unregister(Group)
#admin.site.unregister(User)

admin.site.register(AuthUser, MsicUserAdmin)

#admin.site.register(Client)
#admin.site.register(SmsFac)
#admin.site.register(Appointment)
