from django.contrib.postgres.fields import ArrayField
from django.db import models
from companies.models import Company
from products.models import Product
from django.db import models
# Create your models here.


class ProformaInvoice(models.Model):
    proformaInvoice = models.TextField()
    proformaDate = models.DateField()
    otherReferences = models.TextField(blank=True, null=True)
    customerId = models.ForeignKey(Company, on_delete=models.CASCADE)
    termsOfPayment = models.TextField(blank=True, null=True)
    deliveryTerms = models.TextField(blank=True, null=True)
    preCarriage = models.TextField(blank=True, null=True)
    vesselFlightNo = models.TextField(blank=True, null=True)
    placeOfReceipt = models.TextField(blank=True, null=True)
    portOfLoading = models.TextField(blank=True, null=True)
    portOfDischarge = models.TextField(blank=True, null=True)
    finalDestination = models.TextField(blank=True, null=True)
    products = models.TextField()
    currency = models.TextField()
    totalSales = models.TextField()
    descriptionOfGoods = models.TextField(default="LAMINATED LEAF SPRINGS & NUT WITH BOLTS")


    def __str__(self):
        return str(self.proformaInvoice)
