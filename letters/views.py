from math import ceil

from django.shortcuts import render
from django.http import HttpResponse
from master.models import Bill
from companies.models import Company
from products.models import Product
import json
import datetime
from dateutil.parser import parse
import re

# Create your views here.
def index(request):
    return render(request, "letters/home.html")


def showBills(request):
    context = dict()

    datFrom = request.POST.get("billDateFrom")
    datTo = request.POST.get("billDateTo")
    instance = Bill.objects.filter(billDate__range=[datFrom, datTo])

    context["bills"] = instance

    return render(request, "letters/home.html", context)


def addData(request):
    bill = Bill.objects.get(id=request.POST.get("id"))
    bill.lcNo = request.POST.get("lcNo")
    bill.lcDate = request.POST.get("lcDate")

    if not bill.lcDate:
        bill.lcDate = None

    bill.contractNo = request.POST.get("contractNo")
    bill.contractDate = request.POST.get("contractDate")

    if not bill.contractDate:
        bill.contractDate = None

    bill.shippingBillNo = request.POST.get("shippingBillNo")
    bill.shippingBillDate = request.POST.get("shippingDate")

    if not bill.shippingBillDate:
        bill.shippingBillDate = None

    bill.exchangeNo = request.POST.get("exchangeNo")
    bill.exchangeDate = request.POST.get("exchangeDate")

    if not bill.exchangeDate:
        bill.exchangeDate = None

    bill.consigneeBank = request.POST.get("consigneBank")
    bill.consigneeAccount = request.POST.get("consigneAccount")
    try:
        bill.save()
    finally:
        context = dict()
        dat = bill.billDate
        instance = Bill.objects.filter(billDate=dat)
        context["bills"] = instance
        return render(request, "letters/home.html", context)


def bankLetter(request):
    instance = Bill.objects.get(id=request.GET.get("id"))
    return render(request, 'letters/bankLetter.html', {"bill": instance})


def exportDeclaration(request):
    instance = Bill.objects.get(id=request.GET.get("id"))
    p = re.compile('(?<!\\\\)\'')
    instance.products = p.sub('\"', instance.products)
    instance.products = json.loads(instance.products)
    totalWeight = 0

    for i in instance.products:
        totalWeight += float(i["qty"]) * float(i["weight"])

    return render(request, 'letters/exportDeclaration.html', {"bill": instance, "totalWeight": totalWeight})


def billOfExchange(request):
    instance = Bill.objects.get(id=request.GET.get("id"))
    return render(request, 'letters/billOfExchange.html', {"bill": instance})


def bankLetter2(request):
    instance = Bill.objects.get(id=request.GET.get("id"))
    return render(request, 'letters/bankLetter2.html', {"bill": instance})


def shipmentLetter(request):
    instance = Bill.objects.get(id=request.GET.get("id"))
    return render(request, 'letters/shipmentLetter.html', {"bill": instance})


def edit(request):
    id = request.GET.get("id")
    bill = Bill.objects.get(id=id)
    try:
        bill.lcDate = bill.lcDate.isoformat()
        bill.contractDate = bill.contractDate.isoformat()
        bill.shippingBillDate = bill.shippingBillDate.isoformat()
        bill.exchangeDate = bill.exchangeDate.isoformat()
    finally:
        return render(request, "letters/edit.html", {"bill": bill})


def saveEdit(request):
    bill = Bill.objects.get(id=request.POST.get("id"))
    bill.lcNo = request.POST.get("lcNo")
    bill.lcDate = request.POST.get("lcDate")

    if not bill.lcDate:
        bill.lcDate = None

    bill.contractNo = request.POST.get("contractNo")
    bill.contractDate = request.POST.get("contractDate")

    if not bill.contractDate:
        bill.contractDate = None

    bill.shippingBillNo = request.POST.get("shippingBillNo")
    bill.shippingBillDate = request.POST.get("shippingDate")

    if not bill.shippingBillDate:
        bill.shippingBillDate = None

    bill.exchangeNo = request.POST.get("exchangeNo")
    bill.exchangeDate = request.POST.get("exchangeDate")

    if not bill.exchangeDate:
        bill.exchangeDate = None

    bill.consigneeBank = request.POST.get("consigneBank")
    bill.consigneeAccount = request.POST.get("consigneAccount")
    try:
        bill.save()
    finally:
        context = dict()
        dat = bill.billDate
        instance = Bill.objects.filter(billDate=dat)
        context["bills"] = instance
        return render(request, "letters/home.html", context)
