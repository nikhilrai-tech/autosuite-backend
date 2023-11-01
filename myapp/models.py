from django.db import models

class BardRequest(models.Model):
    question = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class BardResponse(models.Model):
    request = models.OneToOneField(BardRequest, on_delete=models.CASCADE)
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)