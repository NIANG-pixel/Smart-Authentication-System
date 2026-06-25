import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class QRAccess(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Le QR code expire après 5 minutes
        expiration_time = self.created_at + timedelta(minutes=5)
        return timezone.now() < expiration_time and not self.is_used

class AccessLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50) # 'ALLOWED', 'EXPIRED', 'INVALID'
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.scanned_at} - {self.status}"