import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse
from .forms import UserRegistrationForm

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    DetailView,
    UpdateView,
    ListView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
# from django.contrib import messages
from .models import User
from .forms import UserRegistrationForm


@login_required
def assign_doctor(request):
    """
    Страница для выбора врача пациентом
    """
    if request.user.role != 'patient':
        messages.error(request, 'Эта страница только для пациентов')
        return redirect('users:dashboard')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        if doctor_id:
            try:
                doctor = get_object_or_404(User, id=doctor_id, role='doctor',
                                           is_active=True)
                request.user.assigned_doctor = doctor
                request.user.save()
                messages.success(request,
                                 f'Врач {doctor.get_full_name()} успешно назначен!')
                return redirect('users:dashboard')
            except Exception as e:
                messages.error(request, f'Ошибка при назначении врача: {e}')

    # Показываем список доступных врачей
    doctors = User.objects.filter(role='doctor', is_active=True)
    return render(request, 'users/assign_doctor.html', {'doctors': doctors})


logger = logging.getLogger('users')

@sensitive_post_parameters('password1', 'password2')
def register(request):
    if request.method == 'POST':
        role = request.POST.get('role', 'patient')
        if role == 'doctor':
            form = DoctorRegistrationForm(request.POST)
        else:
            form = UserRegistrationForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.phone = form.cleaned_data['phone']
                user.role = 'patient'
                user.save()

                logger.info(f"Успешная регистрация пользователя: {user.username}")
                messages.success(request, 'Регистрация успешно завершена! Теперь вы можете войти.')

                return redirect('login')
            except Exception as e:
                logger.error(f"Ошибка при сохранении пользователя: {e}")
                messages.error(request,f'Произошла ошибка при регистрации: {e}')
                # Явно возвращаем render с формой
                return render(request, 'users/register.html', {'form': form})
        else:
            logger.warning(f"Невалидная форма регистрации: {form.errors}")
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            # Явно возвращаем render с формой
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegistrationForm()

    # Явно возвращаем render для GET-запросов
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        if hasattr(self.request, 'user'):
            self.request.user.delete()
        return super().form_valid(form)

class CustomLogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect('home')

    def get(self, request, *args, **kwargs):
        return render(request, 'main/logout_confirm.html')

class UserDashboardView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/dashboard.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # # Добавляем детализированные данные для отладки
        # debug_data = {
        #     'user_data': {
        #         'id': user.id,
        #         'username': user.username,
        #         'role': user.role,
        #         'assigned_doctor_id': user.assigned_doctor.id if user.assigned_doctor else None,
        #         'is_active': user.is_active
        #     },
        #     'doctor_data': {
        #         'id': user.assigned_doctor.id if user.assigned_doctor else None,
        #         'username': user.assigned_doctor.username if user.assigned_doctor else None,
        #         'specialization': user.assigned_doctor.specialization if user.assigned_doctor else None
        #     } if user.assigned_doctor else None
        # }
        # context['debug_info'] = debug_data


        # # Добавляем все переменные окружения для отладки
        # # context['django_ctx'] = dict(self.request.META)

        # context['is_doctor'] =  user.role == 'doctor'
        # # Добавляем информацию о враче для пациента
        # if user.role == 'patient' and user.assigned_doctor:
        #     context['doctor'] = user.assigned_doctor

        # # Для врачей добавляем количество непрочитанных сообщений (пример)
        # if user.role == 'doctor':
        #     from messaging.models import PrivateMessage
        #     context['unread_messages_count'] = PrivateMessage.objects.filter(
        #         recipient=user,
        #         is_read=False
        #     ).count()

        # return context

class PatientListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        if self.request.user.role == 'doctor':
            return self.request.user.doctor_patients.all()
        return User.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Мои пациенты"
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'specialization']
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:dashboard')

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role != 'doctor':
            form.fields.pop('specialization', None)
        return form

class AssignPatientsView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.role != 'admin':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        doctors = User.objects.filter(role='doctor')
        patients = User.objects.filter(role='patient', assigned_doctor__isnull=True)
        return render(request, 'users/assign_patients.html', {
            'doctors': doctors,
            'patients': patients
        })

    def post(self, request):
        doctor_id = request.POST.get('doctor')
        patient_ids = request.POST.getlist('patients')
        
        doctor = User.objects.get(pk=doctor_id, role='doctor')
        patients = User.objects.filter(pk__in=patient_ids, role='patient')
        
        for patient in patients:
            if patient.assigned_doctors.count() < 10:
                patient.assigned_doctor = doctor
                patient.save()
            else:
                messages.warning(
                    request,
                    f'Пациент {patient} уже прикреплён к максимальному количеству врачей (10)'
                )
        
        return redirect('users:assign_patients')