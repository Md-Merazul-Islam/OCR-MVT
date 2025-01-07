from django.db import models

# Create your models here.
class StudentResult(models.Model):
    roll_number = models.CharField(max_length=6, unique=True)
    gpa = models.FloatField(null=True, blank=True)
    is_passed = models.BooleanField(default=True)
    failed_subjects = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.roll_number
    
    
    
    