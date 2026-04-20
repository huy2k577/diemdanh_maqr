from django.db import models

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    
    class Meta:
        db_table = 'admins'
        managed = False

    def __str__(self):
        return self.full_name