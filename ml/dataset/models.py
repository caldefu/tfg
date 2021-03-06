from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import misaka
User = get_user_model()

def user_directory_path (instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Dataset (models.Model):
    user = models.ForeignKey(User, related_name='datasets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False)
    archivo = models.FileField(upload_to=user_directory_path, null=False)
    arbol = models.TextField(blank=True, default='')



    def __str__ (self):
        return self.name
    
    def save (self, *args, **kwargs):
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.archivo.delete()
        super().delete(*args, **kwargs)
    
    def user_directory_path (instance, filename):
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    class Meta:
        unique_together = ['user', 'name']
        ordering = ['-created_at']