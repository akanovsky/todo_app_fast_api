# tasks/views.py
from django.shortcuts import render
from django.views.generic import ListView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin # Nový import


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Vrátí pouze úkoly patřící aktuálně přihlášenému uživateli
        return Task.objects.filter(user=self.request.user)