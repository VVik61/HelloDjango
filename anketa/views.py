from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import AnketaForm
from .models import Anketa, Question

class AnketaView(FormView):
    template_name = 'anketa/form.html'
    form_class = AnketaForm
    success_url = reverse_lazy('anketa:success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(is_active=True).order_by('order')
        return context

    def form_valid(self, form):
        anketa = Anketa.objects.create(
            full_name=form.cleaned_data['full_name'],
            birth_date=form.cleaned_data['birth_date'],
            gender=form.cleaned_data['gender']
        )
        anketa.generate_answers_text(form.cleaned_data)
        # anketa.save_answers(self.request.POST)
        return super().form_valid(form)

def success_view(request):
    return render(request, 'anketa/success.html')