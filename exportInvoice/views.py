import json
from math import ceil
from django.http.response import HttpResponse
import pandas as pd
from django.shortcuts import render
from pandas.core import indexing
from master.models import Bill
import re


def index(request):
    return render(request, "exportInvoice/home.html")


def showBills(request):
    context = dict()

    datFrom = request.POST.get("billDateFrom")
    datTo = request.POST.get("billDateTo")
    instance = Bill.objects.filter(billDate__range=[datFrom, datTo])

    for bill in instance:
        prod = dict()

        p = re.compile('(?<!\\\\)\'')
        bill.products = p.sub('\"', bill.products)
        bill.products = json.loads(bill.products)

        for product in bill.products:
            p = prod.get(product["name"])

            if p:
                prod[product["name"]]["qty"] += int(product["qty"])
                prod[product["name"]]["netWt"] += float(product["qty"]) * float(product["weight"])
                prod[product["name"]]["totalAmount"] += float(product["cpp"]) * float(product["qty"])
            else:
                prod[product["name"]] = {"hsnCode": product["hsnCode"],
                                         "netWt": float(product["qty"]) * float(product["weight"]),
                                         "qty": int(product["qty"]), "cpp": float(product["cpp"]),
                                         "totalAmount": float(product["cpp"]) * float(product["qty"])}
        bill.products = prod
    context["bills"] = instance
    return render(request, "exportInvoice/home.html", context)


def showPdf(request):
    context = dict()
    id = request.GET.get("id")
    instance = Bill.objects.get(id=id)

    p = re.compile('(?<!\\\\)\'')
    instance.products = p.sub('\"', instance.products)
    instance.products = json.loads(instance.products)

    netWt = 0
    netGrossWt = 0
    lst = []

    # allProds = []
    prod = dict()
    for product in instance.products:
        p = prod.get(product["name"])

        if p:
            prod[product["name"]]["qty"] += int(product["qty"])
            prod[product["name"]]["netWt"] += float(product["qty"]) * float(product["weight"])
            prod[product["name"]]["totalAmount"] += float(product["cpp"]) * float(product["qty"])
            prod[product["name"]]["boxWt"] += float(product["boxWt"])
        else:
            prod[product["name"]] = {"hsnCode": product["hsnCode"],
                                     "netWt": float(product["qty"]) * float(product["weight"]),
                                     "qty": int(product["qty"]), "cpp": float(product["cpp"]),
                                     "totalAmount": float(product["cpp"]) * float(product["qty"]),
                                     "boxWt": float(product["boxWt"])}

    for product, details in prod.items():
        netWt += details["netWt"]
        netGrossWt += details["netWt"]
        netGrossWt += details["boxWt"]
        lst.append({product: details})

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

    x = range(len(prodList) + len(lastList) + 1, int((len(prodList) + len(lastList) + 11)/12)*12)

    context = {
        "iProds": prodList, "eProds": lastList, "netWt": netWt, "netGrossWt": netGrossWt,
        "totalBoxes": instance.totalBoxes, "invoice": instance.invoice, "billDate": instance.billDate,
        "otherReferences": instance.otherReferences, 'grNo': instance.grNo, "customerId": instance.getConsignee(),
        "termOfPayment": instance.termsOfPayment, "preCarriage": instance.preCarriage,
        "billOfLadingNo": instance.billOfLadingNo, "ladingDate": instance.ladingDate,
        "vesselFlightNo": instance.vesselFlightNo, "portOfLoading": instance.portOfLoading,
        "portOfDischarge": instance.portOfDischarge, "finalDestination": instance.finalDestination,
        "natureOfContract": instance.natureOfContract, "currency": instance.currency,
        "freightCharges": instance.freightCharges, "descriptionOfGoods": instance.descriptionOfGoods, "billId": id, "currencyCode": instance.currency.split(" - ")[1], 
        "fractionalCurrencyCode": FractionalCurrencyCode, "nextLevel": len(lastList) > 0, "empty": x, "shippingMark": instance.shipingMark(), "cf_fob": instance.checkerCForFOB(), "amtDesc": instance.amtDescription(), "flag": int(instance.flag), "otherThanConsignee": instance.otherThanConsigne, "discount": instance.discount, "withComponents": instance.withComponents, "descri": instance.descri,
    }
    
    return render(request, 'exportInvoice/pdf_template.html', context)


def changeDescription(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    instance.descriptionOfGoods = val
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))

def changeDescri(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    instance.descri = val
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))

def changeWithComponents(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    instance.withComponents = val
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))

def changeShippingMark(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    instance.shipMark = val
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))


def changeCFFOB(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    instance.checkerForCForFOB = val
    instance.flag = True
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))

def changeAmtDesc(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    instance.amtDesc = val
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))


def updatecompName(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    data = instance.getConsignee()
    data["name"] = val
    instance.pdfConsignee = json.dumps(data)
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))


def updateAddress(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    data = instance.getConsignee()
    data["address"] = val
    data["split_address"] = (len(val)>60)
    instance.pdfConsignee = json.dumps(data)
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))


def updateCountry(request):
    id = request.GET.get("id")
    val = request.GET.get("val")
    instance = Bill.objects.get(id=id)
    data = instance.getConsignee()
    data["country"] = val
    instance.pdfConsignee = json.dumps(data)
    instance.save()
    return HttpResponse(json.dumps({"success": "success"}))
