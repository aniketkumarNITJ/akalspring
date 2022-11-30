import datetime
from math import ceil
import re
from django.shortcuts import render
from django.http import HttpResponse
from .models import Bill
from companies.models import Company
from products.models import Product
import json
from django.db.models import Q


# Create your views here.
def index(request):
    context = dict()
    dat = request.POST.get("billDate")

    instance = Product.objects.all().order_by("product_name")
    context["products"] = instance

    instance = Company.objects.all().order_by("company_name")

    context["companies"] = instance

    return render(request, "master/home.html", context)


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

    instance = Product.objects.all().order_by("product_name")
    context["products"] = instance

    instance = Company.objects.all().order_by("company_name")
    context["companies"] = instance

    return render(request, "master/home.html", context)


def showBills2(request):
    context = dict()

    billDate = request.POST.get("billDate")
    instance = Bill.objects.filter(billDate=billDate)

    for i in instance:
        p = re.compile('(?<!\\\\)\'')
        i.products = p.sub('\"', i.products)
        i.products = json.loads(i.products)

    context["bills"] = instance

    instance = Product.objects.all().order_by("product_name")
    context["products"] = instance

    instance = Company.objects.all().order_by("company_name")
    context["companies"] = instance

    return render(request, "master/home.html", context)


def addBill(request):
    currYear = datetime.datetime.now().year
    currMonth = datetime.datetime.now().month
    if currMonth < 4:
        currYear -= 1
    invoice = "ASL/" + str(Bill.objects.filter(billDate__range=[datetime.date(currYear, 4, 1), datetime.date(currYear+1, 3, 31)]).count()+1) + \
        "/" + str(currYear) + "-" + str(currYear + 1)
    totalBoxes = 0
    totalSales = 0
    billDate = request.POST.get("billDate")
    otherReferences = request.POST.get("otherReferences")
    billOfLadingNo = request.POST.get("billOfLadingNo")
    ladingDate = request.POST.get("ladingDate")

    if not ladingDate:
        ladingDate = None

    customerId = request.POST.get("customerId")

    for char in customerId:
        if char in "'":
            customerId.replace(char, '')

    customerId = Company(company_name=customerId)
    termsOfPayment = request.POST.get("termsOfPayment")
    natureOfContract = request.POST.get("natureOfContract")
    preCarriage = request.POST.get("preCarriage")
    grNo = request.POST.get("grNo")
    vesselFlightNo = request.POST.get("vesselFlightNo")
    portOfLoading = request.POST.get("portOfLoading")
    portOfDischarge = request.POST.get("portOfDischarge")
    finalDestination = request.POST.get("finalDestination")
    freightCharges = request.POST.get("freightCharges")
    currency = request.POST.get("currency")
    totalSales += float(freightCharges)
    totalProds = int(request.POST.get("totalProds"))
    otherThanConsigne = request.POST.get("otherThanConsigne")
    discount = int(request.POST.get("discount"))
    prods = []
    for i in range(1, totalProds+1):
        prod = request.POST.get("productId" + str(i)).replace("\'", "\"")
        prod = json.loads(prod)
        prod["qty"] = request.POST.get("qty" + str(i))
        prod["cpp"] = request.POST.get("cpp" + str(i))
        prod["boxWt"] = request.POST.get("boxWt" + str(i))
        totalSales += float(prod["qty"]) * float(prod["cpp"])
        if float(prod["boxWt"]):
            totalBoxes += 1
        prod["boxType"] = request.POST.get(
            "boxType" + str(i)) + ' ' + str(totalBoxes)
        prods.append(prod)
    prods = json.dumps(prods)
    newBill = Bill(invoice=invoice, billDate=billDate, otherReferences=otherReferences, grNo=grNo,
                   billOfLadingNo=billOfLadingNo, totalBoxes=totalBoxes, ladingDate=ladingDate, customerId=customerId,
                   termsOfPayment=termsOfPayment, natureOfContract=natureOfContract, preCarriage=preCarriage,
                   vesselFlightNo=vesselFlightNo, portOfLoading=portOfLoading, portOfDischarge=portOfDischarge,
                   finalDestination=finalDestination, products=prods, freightCharges=freightCharges, currency=currency,
                   totalSales=totalSales, otherThanConsigne=otherThanConsigne, discount=discount)

    try:
        newBill.save()
    finally:
        return showBills2(request)


def deleteBill(request):
    billId = request.POST.get("id")

    try:
        Bill.objects.filter(id=billId).delete()
        return HttpResponse("Bill Successfully Deleted")
    except:
        return HttpResponse("Bill Deletion Failed")


def editBill(request):
    id = request.GET.get("id")
    bill = Bill.objects.get(id=id)
    company = Company.objects.filter(~Q(company_name=bill.customerId)).order_by("company_name")
    product = Product.objects.all().order_by("product_name")
    p = re.compile('(?<!\\\\)\'')
    bill.products = p.sub('\"', bill.products)
    bill.products = json.loads(bill.products)
    try:
        bill.billDate = bill.billDate.isoformat()
        bill.ladingDate = bill.ladingDate.isoformat()
    finally:
        return render(request, "master/edit.html", {"bill": bill, "companies": company, "products": product})


def editSave(request):
    id = request.POST.get("id")
    bill = Bill.objects.get(id=id)

    totalBoxes = 0
    totalSales = 0
    billDate = request.POST.get("billDate")
    otherReferences = request.POST.get("otherReferences")
    billOfLadingNo = request.POST.get("billOfLadingNo")
    ladingDate = request.POST.get("ladingDate")
    otherThanConsigne = request.POST.get("otherThanConsigne")

    if not ladingDate:
        ladingDate = None

    customerId = request.POST.get("customerId")

    for char in customerId:
        if char in "'":
            customerId.replace(char, '')

    customerId = Company(company_name=customerId)
    termsOfPayment = request.POST.get("termsOfPayment")
    natureOfContract = request.POST.get("natureOfContract")
    preCarriage = request.POST.get("preCarriage")
    grNo = request.POST.get("grNo")
    vesselFlightNo = request.POST.get("vesselFlightNo")
    portOfLoading = request.POST.get("portOfLoading")
    portOfDischarge = request.POST.get("portOfDischarge")
    finalDestination = request.POST.get("finalDestination")
    freightCharges = request.POST.get("freightCharges")
    currency = request.POST.get("currency")
    discount = request.POST.get("discount")
    totalSales += float(freightCharges)
    totalProds = int(request.POST.get("totalProds"))
    prods = []
    for i in range(1, totalProds + 1):
        prod = request.POST.get("productId" + str(i)).replace("\'", "\"")
        prod = json.loads(prod)
        prod["qty"] = request.POST.get("qty" + str(i))
        prod["cpp"] = request.POST.get("cpp" + str(i))
        prod["boxWt"] = request.POST.get("boxWt" + str(i))
        totalSales += float(prod["qty"]) * float(prod["cpp"])
        if float(prod["boxWt"]):
            totalBoxes += 1
        prod["boxType"] = request.POST.get(
            "boxType" + str(i)) + ' ' + str(totalBoxes)
        prods.append(prod)
    prods = json.dumps(prods)

    bill.billDate = billDate

    # currYear = int(billDate[:4])
    # currMonth = int(billDate[5:7])
    # if currMonth < 4:
    #     currYear-=1
    # invoice = "ASL/" + str(97) + "/" + str(currYear) + "-" + str(currYear + 1)
    # print(invoice)
    # bill.invoice=invoice

    bill.otherReferences = otherReferences
    bill.grNo = grNo
    bill.customerId = customerId
    bill.termsOfPayment = termsOfPayment
    bill.natureOfContract = natureOfContract
    bill.preCarriage = preCarriage
    bill.vesselFlightNo = vesselFlightNo
    bill.portOfLoading = portOfLoading
    bill.portOfDischarge = portOfDischarge
    bill.finalDestination = finalDestination
    bill.products = prods
    bill.freightCharges = freightCharges
    bill.totalSales = totalSales
    bill.currency = currency
    bill.totalBoxes = totalBoxes
    bill.billOfLadingNo = billOfLadingNo
    bill.ladingDate = ladingDate
    bill.discount = discount
    bill.otherThanConsigne = otherThanConsigne
    bill.save()
    return showBills2(request)
