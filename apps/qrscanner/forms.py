from django import forms


class ScanPasswordForm(forms.Form):
    schedule_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập mật khẩu'
        })
    )