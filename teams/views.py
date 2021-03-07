from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from . import mixins
from . import models


class TeamListView(CreateView, ListView):
    fields = ("name", "practice_location", "coach")
    context_object_name = 'teams'
    model = models.Team
    template_name = "teams/team_list.html"


class TeamDetailView(DetailView, UpdateView):
    fields = ("name", "practice_location", "coach")
    model = models.Team
    template_name = "teams/team_detail.html"


class TeamCreateView(LoginRequiredMixin, mixins.PageTitleMixin, CreateView):
    fields = ("name", "practice_location", "coach")
    model = models.Team
    page_title = "Create A New Team"

    def get_initial(self):
        initial = super().get_initial()
        initial['coach'] = self.request.user.pk
        return initial


class TeamUpdateView(LoginRequiredMixin, mixins.PageTitleMixin, UpdateView):
    fields = ("name", "practice_location", "coach")
    model = models.Team
    
    def get_page_title(self):
        obj = self.get_object()
        return "Update {}".format(obj)


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Team
    success_url = reverse_lazy("teams:list")

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(coach=self.request.user)
        return self.model.objects.all()


