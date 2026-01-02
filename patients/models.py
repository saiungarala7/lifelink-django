from django.db import models
from accounts.models import User


class PatientProfile(models.Model):
    """
    Extended profile for Patient users
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )

    # Basic Information
    phone_number = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        blank=True,
        null=True
    )

    blood_group = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )

    # Address
    address = models.TextField(blank=True, null=True)

    # Profile Picture
    profile_image = models.ImageField(
        upload_to='patient_profiles/',
        blank=True,
        null=True
    )

    # Additional Information
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.user.username
