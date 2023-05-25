from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import AddLeadForm

@login_required
def add_lead(request):
    form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form
    })