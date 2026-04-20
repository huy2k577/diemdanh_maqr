from django.urls import path
from .views import enter_password_view, scan_page_view, save_scan_view

app_name = 'qrscanner'

urlpatterns = [
    path('<int:schedule_id>/login/', enter_password_view, name='loginscarner'),
    path('<int:schedule_id>/', scan_page_view, name='scan_page'),
    path('<int:schedule_id>/save/', save_scan_view, name='save_scan'),
]