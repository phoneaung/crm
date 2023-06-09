from django.urls import path

from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('add-lead/', views.add_lead, name='add'),
    path('<int:pk>/delete/', views.leads_delete, name='delete'),
    path('<int:pk>/edit/', views.leads_edit, name='edit'),
    path('<int:pk>/convert', views.leads_convert, name='convert'),
]