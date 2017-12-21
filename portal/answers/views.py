# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import PublicContrib
from .forms import PublicContribCreateForm
from django.urls import reverse_lazy
# Create your views here.


class PublicContribListView(ListView):
    def get_queryset(self):
        try:
            combined_queryset = PublicContrib.objects.filter(owner=self.request.user) |\
                                PublicContrib.objects.filter(ispublic=True)
        except TypeError:
            combined_queryset = PublicContrib.objects.filter(ispublic=True)
        return combined_queryset


class PublicContribDetailView(DetailView):
    def get_queryset(self):
        try:
            combined_queryset = PublicContrib.objects.filter(owner=self.request.user) |\
                                PublicContrib.objects.filter(ispublic=True)
        except TypeError:
            combined_queryset = PublicContrib.objects.filter(ispublic=True)
        return combined_queryset


class PublicContribDeletelView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        combined_queryset = PublicContrib.objects.filter(owner=self.request.user, ispublic=False)
        return combined_queryset
    success_url = reverse_lazy('answers:index')


class PublicContribCreateView(LoginRequiredMixin, CreateView):
    form_class = PublicContribCreateForm
    template_name = 'form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(PublicContribCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PublicContribCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create'
        return context

    def get_form_kwargs(self):
        kwargs = super(PublicContribCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs


class PublicContribUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PublicContribCreateForm
    template_name = 'form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PublicContribUpdateView, self).get_context_data(*args, **kwargs)
        shortname = self.get_object().shortname
        context['title'] = f'Update Name: {shortname}'
        return context

    def get_queryset(self):
        return PublicContrib.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(PublicContribUpdateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs