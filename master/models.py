from typing import Tuple
from django.contrib.postgres.fields import ArrayField
from django.db import models
from companies.models import Company
from products.models import Product
from django.db import models
import json
import pandas as pd
# Create your models here.


class Bill(models.Model):
    invoice = models.TextField()
    billDate = models.DateField()
    otherReferences = models.TextField(blank=True, null=True)
    grNo = models.TextField(blank=True, null=True)
    customerId = models.ForeignKey(Company, on_delete=models.CASCADE)
    otherThanConsigne = models.TextField(default="None")
    termsOfPayment = models.TextField(blank=True, null=True)
    natureOfContract = models.TextField(blank=True, null=True)
    preCarriage = models.TextField(blank=True, null=True)
    vesselFlightNo = models.TextField(blank=True, null=True)
    portOfLoading = models.TextField(blank=True, null=True)
    portOfDischarge = models.TextField(blank=True, null=True)
    finalDestination = models.TextField(blank=True, null=True)
    products = models.TextField()
    freightCharges = models.FloatField()
    totalSales = models.FloatField()
    currency = models.TextField()
    ladingDate = models.DateField(blank=True, null=True)
    billOfLadingNo = models.TextField(blank=True, null=True)
    totalBoxes = models.IntegerField()
    discount = models.FloatField(default=0)
    # for letters
    lcNo = models.TextField(blank=True, null=True)
    lcDate = models.DateField(blank=True, null=True)
    contractNo = models.TextField(blank=True, null=True)
    contractDate = models.DateField(blank=True, null=True)
    shippingBillNo = models.TextField(blank=True, null=True)
    shippingBillDate = models.DateField(blank=True, null=True)
    exchangeNo = models.TextField(blank=True, null=True)
    exchangeDate = models.DateField(blank=True, null=True)
    consigneeBank = models.TextField(blank=True, null=True)
    consigneeAccount = models.TextField(blank=True, null=True)
    descriptionOfGoods = models.TextField(
        default="LAMINATED LEAF SPRINGS & NUT WITH BOLTS")
    shipMark = models.TextField(blank=True, null=True)
    checkerForCForFOB = models.TextField(blank=True, null=True)
    amtDesc = models.TextField(blank=True, null=True)
    pdfConsignee = models.TextField(blank=True, null=True)
    flag = models.BooleanField(default=False)
    withComponents = models.TextField(
        default="(With Components)", blank=True, null=True)
    descri = models.TextField(default="(add description)")

    def shipingMark(self):
        if self.shipMark:
            return self.shipMark
        else:
            self.shipMark = (
                "1 - {} {}".format(self.totalBoxes, self.finalDestination))
            self.save()
            return self.shipMark

    def amtDescription(self):
        if self.amtDesc:
            return self.amtDesc
        else:
            self.amtDesc = ("Total {} FOB".format(
                self.currency.split(" - ")[1]))
            self.save()
            return self.amtDesc

    def getConsignee(self):
        if self.pdfConsignee:
            return json.loads(self.pdfConsignee)
        else:
            if len(self.customerId.company_address) > 60:
                ind = 0

                for i in range(25, len(self.customerId.company_address)):
                    if self.customerId.company_address[i] == ' ':
                        ind = i
                        break

                self.pdfConsignee = json.dumps({
                    'name': self.customerId.company_name,
                    'address1': self.customerId.company_address[:ind],
                    'address2': self.customerId.company_address[ind+1:],
                    'country': self.customerId.company_country,
                    'split_address': 1,
                })
            else:
                self.pdfConsignee = json.dumps({
                    'name': self.customerId.company_name,
                    'address': self.customerId.company_address,
                    'country': self.customerId.company_country,
                    'split_address': 0,
                })

            self.save()
            return json.loads(self.pdfConsignee)

    def checkerCForFOB(self):
        if self.checkerForCForFOB and (self.checkerForCForFOB != "FOB" and self.checkerForCForFOB != "C&F"):
            return self.checkerForCForFOB
        else:
            self.checkerForCForFOB = "Total C&F PORT {} {} ".format(
                self.portOfDischarge, self.currency)
            self.save()
            return self.checkerForCForFOB

    def __str__(self):
        return str(self.invoice)
