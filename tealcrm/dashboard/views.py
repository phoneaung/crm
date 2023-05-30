from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from client.models import Client
from lead.models import Lead
from team.models import Team

@login_required
def dashboard(request):
    team = pass

    # make these lists order by (-Created at) and show five of them 
    leads = pass
    clients = pass

    return render(request, 'dashboard/dashboard.html', {
        'leads': lead,
        'clients': client
    })
