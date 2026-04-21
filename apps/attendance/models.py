from django.db import models
from apps.accounts.models import Admin

class ScanSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(
        Admin,
        on_delete=models.CASCADE,
        db_column='admin_id',
        related_name='scan_schedules',
        null=True,
        blank=True
    )
    topic_name = models.CharField(max_length=255)
    scan_date = models.DateField()
    scan_password = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'scan_schedules'
        managed = True
        ordering = ['-id']

    def __str__(self):
        return self.topic_name
    

class ScanHistory(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(
        ScanSchedule,
        on_delete=models.CASCADE,
        db_column='schedule_id',
        related_name='scan_histories',
        null=True,
        blank=True
    )
    masv = models.CharField(max_length=20)
    tensv = models.CharField(max_length=100)
    namsinhsv = models.DateField()

    class Meta:
        db_table = 'scan_histories'
        managed = True
        constraints = [
            models.UniqueConstraint(fields=['schedule', 'masv'], name='uq_schedule_masv')
        ]

    def __str__(self):
        return f'{self.masv} - {self.tensv}'