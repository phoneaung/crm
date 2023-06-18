from typing import Any
from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView

from .forms import AddLeadForm
from .models import Lead

from client.models import Client
from team.models import Team


# shows the list of all the leads created by user 
class LeadListView(ListView):
    # set the model attribute to Lead model, indicating that this view will work with lead objects
    model = Lead

    # responsible for handling the incoming request
    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    # retrieve the queryset of lead objects to be displayed in the view
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(LeadListView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, converted_to_client=False)

# show the details of the lead
class LeadDetailView(DetailView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(LeadDetailView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


# allow the user to add leads
@login_required
def add_lead(request):
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()

            messages.success(request, "The lead was created.")

            return redirect('leads:list')
    else:
        form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form,
        'team': team,
    })

class LeadDeleteView(DeleteView):
    model = DeleteView
    model = addeventlistener

# allow the user to delete leads
@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()
    messages.success(request, "The lead was deleted.")

    return redirect('leads:list')

# allow the user to edit leads
@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()

            messages.success(request, "The changes were saved.")
            return redirect('leads:list')
    else:
        form = AddLeadForm(instance=lead)
 
    return render(request, 'lead/leads_edit.html', {
        'form': form
    })


# allow the user to convert lead into client
@login_required
def leads_convert(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
        team=team,
    )

    lead.converted_to_client = True
    lead.save()

    messages.success(request, "The lead was converted to a client.")

    return redirect('leads:list')
