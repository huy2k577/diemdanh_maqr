from django.db import migrations

def create_admin(apps, schema_editor):
    Admin = apps.get_model('accounts', 'Admin')
    
    if not Admin.objects.filter(username='admin').exists():
        Admin.objects.create(
            username='admin',
            password='123456',
            full_name='T.Duy'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]