from django.urls import path
from .views import AuditoriaListView, AuditoriaDetailView

app_name = "auditoria"

urlpatterns = [
    path('', AuditoriaListView.as_view(), name='auditoria_list'),
    path('<int:pk>/', AuditoriaDetailView.as_view(), name='auditoria_detail'),
]