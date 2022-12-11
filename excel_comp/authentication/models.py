from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
