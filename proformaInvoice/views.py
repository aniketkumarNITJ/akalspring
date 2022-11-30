import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse
from companies.models import Company
from products.models import Product
from .models import ProformaInvoice
from django.db.models import Q
import pandas as pd
import re

# Create your views here.


def index(request):
    context = dict()
    dat = request.POST.get("billDate")

    instance = Product.objects.all()
    context["products"] = instance

    instance = Company.objects.all()
    context["companies"] = instance

    return render(request, "proformaInvoice/home.html", context)


def showBills(request):
    context = dict()

    datFrom = request.POST.get("billDateFrom")
    datTo = request.POST.get("billDateTo")
    instance = ProformaInvoice.objects.filter(
        proformaDate__range=[datFrom, datTo])

    for i in instance:
        p = re.compile('(?<!\\\\)\'')
        i.products = p.sub('\"', i.products)
        i.products = json.loads(i.products)

    context["bills"] = instance

    instance = Product.objects.all()
    context["products"] = instance

    instance = Company.objects.all()
    context["companies"] = instance

    return render(request, "proformaInvoice/home.html", context)


def showBills2(request):
    context = dict()

    proformaDate = request.POST.get("proformaDate")
    instance = ProformaInvoice.objects.filter(proformaDate=proformaDate)

    for i in instance:
        p = re.compile('(?<!\\\\)\'')
        i.products = p.sub('\"', i.products)
        i.products = json.loads(i.products)

    context["bills"] = instance

    instance = Product.objects.all()
    context["products"] = instance

    instance = Company.objects.all()
    context["companies"] = instance

    return render(request, "proformaInvoice/home.html", context)


def addInvoice(request):
    currYear = datetime.datetime.now().year
    invoice = "ASL/" + str(ProformaInvoice.objects.all().count() + 1) + \
        "/" + str(currYear) + "-" + str(currYear + 1)
    billDate = request.POST.get("proformaDate")
    otherReferences = request.POST.get("otherReferences")
    customerId = request.POST.get("customerId")

    for char in customerId:
        if char in "'":
            customerId.replace(char, '')

    customerId = Company(company_name=customerId)
    termsOfPayment = request.POST.get("termsOfPayment")
    deliveryTerms = request.POST.get("deliveryTerms")
    preCarriage = request.POST.get("preCarriage")
    vesselFlightNo = request.POST.get("vesselFlightNo")
    placeOfReceipt = request.POST.get("placeOfReceipt")
    portOfLoading = request.POST.get("portOfLoading")
    portOfDischarge = request.POST.get("portOfDischarge")
    finalDestination = request.POST.get("finalDestination")
    currency = request.POST.get("currency")
    totalProds = int(request.POST.get("totalProds"))
    prods = []
    totalSales = 0
    for i in range(1, totalProds + 1):
        prod = request.POST.get("productId" + str(i)).replace("\'", "\"")
        prod = json.loads(prod)
        prod["qty"] = request.POST.get("qty" + str(i))
        prod["cpp"] = request.POST.get("cpp" + str(i))
        prod["unit"] = request.POST.get("unit" + str(i))
        totalSales += float(prod["qty"]) * float(prod["cpp"])
        prods.append(prod)
    prods = json.dumps(prods)
    proformaInvoice = ProformaInvoice(proformaInvoice=invoice, proformaDate=billDate, otherReferences=otherReferences,
                                      customerId=customerId, termsOfPayment=termsOfPayment,
                                      deliveryTerms=deliveryTerms, preCarriage=preCarriage,
                                      vesselFlightNo=vesselFlightNo, placeOfReceipt=placeOfReceipt,
                                      portOfLoading=portOfLoading, portOfDischarge=portOfDischarge,
                                      finalDestination=finalDestination, products=prods, currency=currency,
                                      totalSales=totalSales)

    try:
        proformaInvoice.save()
    finally:
        return showBills2(request)


def getPdf(request):
    context = dict()
    id = request.GET.get("id")
    instance = ProformaInvoice.objects.get(id=id)
    p = re.compile('(?<!\\\\)\'')
    instance.products = p.sub('\"', instance.products)
    instance.products = json.loads(instance.products)

    lst = list()

    for product in instance.products:
        lst.append(product)

    prodList = []
    while len(lst):
        prods = []
        while len(lst) > 0 and len(prods) < 12:
            prods.append(lst.pop(0))
        prodList.append(prods)

    lastList = prodList[-1]
    prodList = prodList[:-1]

    df = pd.read_csv("currency.csv")
    df = df[df.CurrenyCode == instance.currency.split(" - ")[1]]

    FractionalCurrencyCode = ""

    for i in df["FractionalCurrencyCode"]:
        FractionalCurrencyCode = i
        FractionalCurrencyCode = FractionalCurrencyCode.capitalize()
        break

    x = range(len(prodList) + len(lastList) + 1,
                  int((len(prodList) + len(lastList) + 11)/12)*12)

    context = {
        "iProds": prodList, "eProds": lastList, "invoice": instance.proformaInvoice,
        "billDate": instance.proformaDate, "otherReferences": instance.otherReferences,
        "customerId": instance.customerId, "termOfPayment": instance.termsOfPayment,
        "deliveryTerms": instance.deliveryTerms, "preCarriage": instance.preCarriage,
        "vesselFlightNo": instance.vesselFlightNo, "placeOfReceipt": instance.placeOfReceipt,
        "portOfLoading": instance.portOfLoading, "portOfDischarge": instance.portOfDischarge,
        "finalDestination": instance.finalDestination, "currency": instance.currency,
        "totalSales": instance.totalSales, "billId": id, "descriptionOfGoods": instance.descriptionOfGoods, "currencyCode": instance.currency.split(" - ")[1],
        "fractionalCurrencyCode": FractionalCurrencyCode, "nextLevel": len(lastList) > 0, "empty": x,
    }
    print(context["eProds"])
    return render(request, 'proformaInvoice/pdf_template.html', context)


def deleteBill(request):
    billId = request.POST.get("id")

    try:
        ProformaInvoice.objects.filter(id=billId).delete()
        return HttpResponse("Bill Successfully Deleted")
    except:
        return HttpResponse("Bill Deletion Failed")


def editBill(request):
    id = request.GET.get("id")
    bill = ProformaInvoice.objects.get(id=id)
    company = Company.objects.filter(~Q(company_name=bill.customerId))
    product = Product.objects.all()
    p = re.compile('(?<!\\\\)\'')
    bill.products = p.sub('\"', bill.products)
    bill.products = json.loads(bill.products)
    try:
        bill.proformaDate = bill.proformaDate.isoformat()
    finally:
        print(bill.products)
        return render(request, "proformaInvoice/edit.html", {"bill": bill, "companies": company, "products": product})


def saveEdit(request):
    id = request.POST.get("id")
    bill = ProformaInvoice.objects.get(id=id)
    bill.billDate = request.POST.get("proformaDate")
    bill.otherReferences = request.POST.get("otherReferences")
    customerId = request.POST.get("customerId")

    for char in customerId:
        if char in "'":
            customerId.replace(char, '')

    bill.customerId = Company(company_name=customerId)
    bill.termsOfPayment = request.POST.get("termsOfPayment")
    bill.deliveryTerms = request.POST.get("deliveryTerms")
    bill.preCarriage = request.POST.get("preCarriage")
    bill.vesselFlightNo = request.POST.get("vesselFlightNo")
    bill.placeOfReceipt = request.POST.get("placeOfReceipt")
    bill.portOfLoading = request.POST.get("portOfLoading")
    bill.portOfDischarge = request.POST.get("portOfDischarge")
    bill.finalDestination = request.POST.get("finalDestination")
    bill.currency = request.POST.get("currency")
    totalProds = int(request.POST.get("totalProds"))
    prods = []
    totalSales = 0
    for i in range(1, totalProds + 1):
        prod = request.POST.get("productId" + str(i)).replace("\'", "\"")
        prod = json.loads(prod)
        prod["qty"] = request.POST.get("qty" + str(i))
        prod["cpp"] = request.POST.get("cpp" + str(i))
        prod["unit"] = request.POST.get("unit" + str(i))
        totalSales += float(prod["qty"]) * float(prod["cpp"])
        prods.append(prod)
    bill.products = json.dumps(prods)
    bill.totalSales = totalSales
    try:
        bill.save()
    finally:
        return showBills2(request)


def changeDescription(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = ProformaInvoice.objects.get(id=id)
    instance.descriptionOfGoods = val
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))
