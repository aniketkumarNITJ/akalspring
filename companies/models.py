from django.db import models

# Create your models here.


class Company(models.Model):
    company_name = models.TextField(primary_key=True)
    company_address = models.TextField()
    company_country = models.TextField()

    def __str__(self):
        return self.company_name

