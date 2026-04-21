import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.attendance.models import ScanSchedule, ScanHistory
from .forms import ScanPasswordForm


def enter_password_view(request, schedule_id):
    schedule = get_object_or_404(ScanSchedule, pk=schedule_id, is_active=1)
    form = ScanPasswordForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        password = form.cleaned_data['schedule_password'].strip()

        if password == schedule.scan_password:
            request.session[f'scan_access_{schedule_id}'] = True
            return redirect('qrscanner:scan_page', schedule_id=schedule_id)

        form.add_error('schedule_password', 'Mật khẩu không đúng.')

    return render(request, 'qrscanner/loginscarner.html', {
        'form': form,
        'schedule': schedule
    })


def scan_page_view(request, schedule_id):
    schedule = get_object_or_404(ScanSchedule, pk=schedule_id, is_active=1)

    if not request.session.get(f'scan_access_{schedule_id}'):
        return redirect('qrscanner:loginscarner', schedule_id=schedule_id)

    return render(request, 'qrscanner/scan_page.html', {
        'schedule': schedule
    })


@require_POST
def save_scan_view(request, schedule_id):
    schedule = get_object_or_404(ScanSchedule, pk=schedule_id, is_active=1)

    if not request.session.get(f'scan_access_{schedule_id}'):
        return JsonResponse({
            'success': False,
            'message': 'Bạn chưa xác thực mật khẩu.'
        }, status=403)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu gửi lên không hợp lệ.'
        }, status=400)

    qr_text = data.get('qr_text', '').strip()

    if not qr_text:
        return JsonResponse({
            'success': False,
            'message': 'Không nhận được dữ liệu QR.'
        }, status=400)

    # QR thật: DH52300671_LEPHUOCHUY_22.03.2005
    parts = [item.strip() for item in qr_text.split('_')]

    if len(parts) != 3:
        return JsonResponse({
            'success': False,
            'message': 'Mã QR không đúng định dạng.'
        }, status=400)

    masv, tensv, ngaysinh_text = parts

    try:
        namsinhsv = datetime.strptime(ngaysinh_text, '%d.%m.%Y').date()
    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Ngày sinh không hợp lệ.'
        }, status=400)

    if ScanHistory.objects.filter(schedule_id=schedule_id, masv=masv).exists():
        return JsonResponse({
            'success': False,
            'message': f'Sinh viên đã được quét trước đó.'
        }, status=400)

    try:
        ScanHistory.objects.create(
            schedule=schedule,
            masv=masv,
            tensv=tensv,
            namsinhsv=namsinhsv
        )
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Không thể lưu dữ liệu vào hệ thống: {str(e)}'
        }, status=500)

    return JsonResponse({
        'success': True,
        'message': 'Quét mã thành công.',
        'student': {
            'masv': masv,
            'tensv': tensv,
            'namsinhsv': namsinhsv.strftime('%d/%m/%Y')
        }
    })