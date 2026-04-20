from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminLoginForm
from .models import Admin

def login_view(request):
    if request.session.get('admin_id'):
        return redirect('attendance:dashboard')

    form = AdminLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()

            admin = Admin.objects.filter(username=username, password=password).first()

            if admin:
                request.session['admin_id'] = admin.id
                request.session['admin_name'] = admin.full_name
                return redirect('attendance:dashboard')
            else:
                messages.error(request, 'Sai tài khoản hoặc mật khẩu.')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('accounts:login')