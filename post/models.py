from django.db import models
from account.models import Account


class Post(models.Model):
    # image = models.ImageField(upload_to='stock/images/', blank=True)
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, null=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)
    # file = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"Title: {self.title.__str__()}; Sender: {self.sender.__str__()}"

