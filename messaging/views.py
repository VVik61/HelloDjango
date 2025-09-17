# messaging/views.py
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import PrivateMessage
from .forms import PrivateMessageForm
from users.models import User


class InboxView(LoginRequiredMixin, ListView):
    model = PrivateMessage
    template_name = 'messaging/inbox.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        return PrivateMessage.objects.filter(
            Q(recipient=self.request.user) | Q(sender=self.request.user)
        ).order_by('-timestamp').select_related('sender', 'recipient')



class SendPrivateMessageView(LoginRequiredMixin, CreateView):
    model = PrivateMessage
    form_class = PrivateMessageForm
    template_name = 'messaging/send_message.html'
    success_url = reverse_lazy('messaging:inbox')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        # Если передан recipient_id, устанавливаем получателя
        if 'recipient_id' in self.kwargs:
            recipient = get_object_or_404(User, pk=self.kwargs['recipient_id'])
            kwargs['initial'] = {'recipient': recipient}
            
            # Для пациентов ограничиваем выбор только их врачом
            if self.request.user.role == 'patient' and self.request.user.assigned_doctor:
                kwargs['initial']['recipient'] = self.request.user.assigned_doctor

        return kwargs

    def form_valid(self, form):
        form.instance.sender = self.request.user
        
        # Для пациентов принудительно устанавливаем врача как получателя
        if self.request.user.role == 'patient' and self.request.user.assigned_doctor:
            form.instance.recipient = self.request.user.assigned_doctor
            
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # После того как форма создана, настраиваем queryset в зависимости от роли
        if self.request.user.role == 'patient':
            # Для пациентов показываем только их лечащего врача
            if self.request.user.assigned_doctor:
                form.fields['recipient'].queryset = User.objects.filter(
                    pk=self.request.user.assigned_doctor.pk
                )
            else:
                form.fields['recipient'].queryset = User.objects.none()
            form.fields['recipient'].disabled = True
            
        elif self.request.user.role == 'doctor':
            # Для врачей показываем только их пациентов
            form.fields['recipient'].queryset = self.request.user.doctor_patients.all()
            
        return form


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = PrivateMessage
    template_name = 'messaging/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            Q(recipient=self.request.user) | Q(sender=self.request.user)
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.recipient == self.request.user and not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj

class MessageThreadView(LoginRequiredMixin, ListView):
    template_name = 'messaging/message_thread.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        return PrivateMessage.objects.filter(
            (Q(sender=self.request.user) & Q(recipient=user)) |
            (Q(sender=user) & Q(recipient=self.request.user))
        ).order_by('timestamp').select_related('sender', 'recipient')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_user'] = get_object_or_404(User, pk=self.kwargs['user_id'])
        return context