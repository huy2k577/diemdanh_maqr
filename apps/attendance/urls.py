from django.urls import path
from .views import (
    dashboard_view,
    create_schedule_view,
    edit_schedule_view,
    toggle_schedule_view,
    delete_schedule_view,
    history_list_view,
    export_history_excel_view,
)

app_name = 'attendance'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('create/', create_schedule_view, name='create_schedule'),
    path('edit/<int:pk>/', edit_schedule_view, name='edit_schedule'),
    path('toggle/<int:pk>/', toggle_schedule_view, name='toggle_schedule'),
    path('delete/<int:pk>/', delete_schedule_view, name='delete_schedule'),
    path('history/<int:pk>/', history_list_view, name='history_list'),
    path('export/<int:pk>/', export_history_excel_view, name='export_history_excel'),
]