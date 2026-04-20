from django import forms
from .models import ScanSchedule

class ScanScheduleForm(forms.ModelForm):
    class Meta:
        model = ScanSchedule
        fields = ['topic_name', 'scan_date', 'scan_password', 'is_active']
        widgets = {
            'topic_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên chủ đề điểm danh'
            }),
            'scan_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'scan_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mật khẩu để quét'
            }),
            'is_active': forms.Select(
                choices=[(1, 'Đang hoạt động'), (0, 'Ngưng hoạt động')],
                attrs={'class': 'form-control'}
            )
        }