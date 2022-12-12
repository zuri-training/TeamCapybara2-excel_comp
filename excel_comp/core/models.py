from django.db import models
from django.conf import settings


class document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    file = models.FileField()
    filename = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        if self.filename:
            return self.filename
        return self.user.username
        
