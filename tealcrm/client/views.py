from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddClientForm
from .models import Client

from team.models import Team


# shows the list of all the clients created by user
@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/clients_list.html', {
        'clients': clients
    })


# show the details of a client
@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    return render(request, 'client/clients_detail.html', {
        'client': client
    })


# allow the user to add clients
@login_required
def add_client(request):
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(request, "The client was created.")

            return redirect('clients:list')
    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html', {
        'form': form,
        'team': team,
    })


# allow the user to delete clients
@login_required
def clients_delete(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, "The client was deleted.")

    return redirect('clients:list')


# allow the user to edit leads
@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, "The changes were saved.")
            return redirect('clients:list')
    else:
        form = AddClientForm(instance=client)
 
    return render(request, 'client/clients_edit.html', {
        'form': form
    })
