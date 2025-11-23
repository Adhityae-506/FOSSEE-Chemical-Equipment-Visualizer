# from django.conf import settings
# from django.db import models

# class Dataset(models.Model):
#     owner = models.ForeignKey(
#     settings.AUTH_USER_MODEL,
#     on_delete=models.CASCADE,
#     null=True,
#     blank=True,
# )
#     file_name = models.CharField(max_length=255)
#     upload_time = models.DateTimeField(auto_now_add=True)
#     csv_file = models.FileField(upload_to='datasets/', null=True, blank=True)
#     summary_json = models.JSONField()

#     class Meta:
#         ordering = ['-upload_time']

#     def __str__(self):
#         return f"{self.file_name} ({self.owner})"

from django.db import models

class Dataset(models.Model):
    file_name = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to='datasets/', null=True, blank=True)
    summary_json = models.JSONField()

    class Meta:
        ordering = ['-upload_time']

    def __str__(self):
        return f"{self.file_name}"
