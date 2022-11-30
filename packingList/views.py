import json
from math import ceil
import re
from django.shortcuts import render
from master.models import Bill


def index(request):
    return render(request, "packingList/home.html")


def showBills(request):
    context = dict()

    datFrom = request.POST.get("billDateFrom")
    datTo = request.POST.get("billDateTo")
    instance = Bill.objects.filter(billDate__range=[datFrom, datTo])

    for i in instance:
        p = re.compile('(?<!\\\\)\'')
        i.products = p.sub('\"', i.products)
        i.products = json.loads(i.products)

    context["bills"] = instance

    return render(request, "packingList/home.html", context)


def showPdf(request):
    context = dict()
    id = request.GET.get("id")
    instance = Bill.objects.get(id=id)

    p = re.compile('(?<!\\\\)\'')
    instance.products = p.sub('\"', instance.products)
    instance.products = json.loads(instance.products)

    netWt = 0
    netGrossWt = 0
    lst = list()

    for product in instance.products:
        netWt += float(product["weight"])*float(product["qty"])
        netGrossWt += float(product["weight"]) * \
            float(product["qty"]) + float(product["boxWt"])
        lst.append(product)

    prodList = []
    while len(lst):
        prods = []
        while len(lst) > 0 and len(prods) < 12:
            prods.append(lst.pop(0))
        prodList.append(prods)

    lastList = prodList[-1]
    prodList = prodList[:-1]

    x = range(len(prodList) + len(lastList) + 1,
              int((len(prodList) + len(lastList) + 11)/12)*12)

    context = {
        "iProds": prodList, "eProds": lastList, "netWt": netWt, "netGrossWt": netGrossWt,
        "totalBoxes": instance.totalBoxes, "invoice": instance.invoice, "billDate": instance.billDate,
        "otherReferences": instance.otherReferences, 'grNo': instance.grNo, "customerId": instance.getConsignee(),
        "termOfPayment": instance.termsOfPayment, "preCarriage": instance.preCarriage,
        "billOfLadingNo": instance.billOfLadingNo, "ladingDate": instance.ladingDate,
        "vesselFlightNo": instance.vesselFlightNo, "portOfLoading": instance.portOfLoading,
        "portOfDischarge": instance.portOfDischarge, "finalDestination": instance.finalDestination,
        "natureOfContract": instance.natureOfContract, "billId": id, "nextLevel": len(lastList) > 0, "empty": x,  "descriptionOfGoods": instance.descriptionOfGoods, "shippingMark": instance.shipingMark(), "otherThanConsignee": instance.otherThanConsigne, "withComponents": instance.withComponents
    }
    return render(request, 'packingList/pdf_template.html', context)
