from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    specialty = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50,unique=True)
    years_of_experience = models.IntegerField()
    availability_status=models.CharField(
        max_length=20,
        choices=[
            ('available','Available'),
            ('unavailable','Unavailable')
        ],
        default='available'
    )
    working_hours_start = models.TimeField()
    working_hours_end = models.TimeField()
    average_response_time = models.IntegerField(help_text="Average response time in minutes", default=30)
    rating = models.FloatField(
        validators = [MinValueValidator(0.0),MaxValueValidator(5.0)],
        default=0.0
    )
    total_reviews = models.IntegerField(default=0)
    active_patients = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"DR. {self.user.get_full_name()} - {self.specialty}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['availability_status']),
        ]
    