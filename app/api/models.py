from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract=True
    
    
class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blog")
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField()
    
    
    
        