from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import User

class CustomUserChangeForm(forms.ModelForm):
    doctor_patients = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='patient'),
        required=False,
        label=_('Прикреплённые пациенты')
    )

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.role == 'doctor':
            self.fields['doctor_patients'].initial = self.instance.doctor_patients.all()
        
        if self.instance and self.instance.role != 'doctor':
            self.fields.pop('doctor_patients', None)
            if 'specialization' in self.fields:
                self.fields.pop('specialization')

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            if user.role == 'doctor':
                current_patients = set(user.doctor_patients.all())
                new_patients = set(self.cleaned_data.get('doctor_patients', []))
                
                for patient in current_patients - new_patients:
                    patient.assigned_doctor = None
                    patient.save()
                
                for patient in new_patients - current_patients:
                    if patient.assigned_doctors.count() < 10:
                        patient.assigned_doctor = user
                        patient.save()
                    else:
                        messages.warning(
                            self.request,
                            f'Пациент {patient} уже прикреплён к максимальному количеству врачей (10)'
                        )
        
        return user

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'phone'),
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        
        if obj:
            custom_fieldsets = list(fieldsets)
            
            medical_fields = []
            if obj.role == 'doctor':
                medical_fields.extend(['specialization', 'doctor_patients'])
            elif obj.role == 'patient':
                medical_fields.append('assigned_doctor')
            
            if medical_fields:
                custom_fieldsets.insert(2, (
                    _('Medical info'), 
                    {'fields': medical_fields}
                ))
            
            return custom_fieldsets
        
        return fieldsets
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if obj and obj.role == 'patient' and 'assigned_doctor' in form.base_fields:
            form.base_fields['assigned_doctor'].label = _('Лечащий врач')
            form.base_fields['assigned_doctor'].queryset = User.objects.filter(
                role='doctor'
            )
        
        return form