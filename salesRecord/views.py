import json
from datetime import datetime, date

from django.shortcuts import render
from django.http import HttpResponse
from master.models import Bill
from companies.models import Company
from django.db.models import Sum


# Create your views here.
def index(request):
    allCom = Company.objects.all()
    context = {"companies": allCom, "company": "Company"}
    return render(request, "salesRecord/home.html", context)


def findSalesRecord(request):
    minDate = date(day=31, month=12, year=3000)
    maxDate = date(day=31, month=12, year=1999)
    context = dict()

    instance = Company.objects.all()
    context["companies"] = instance

    instance = Bill.objects.filter(customerId=request.POST.get("company"))

    points = list()

    for bill in instance:
        minDate = min(minDate, bill.billDate)
        maxDate = max(maxDate, bill.billDate)
        points.append({'x': bill.billDate, 'y': bill.totalSales})
        context["currency"] = bill.currency

    context["points"] = points
    context["minDate"] = minDate
    context["maxDate"] = maxDate
    context["company"] = request.POST.get("company")

    return render(request, "salesRecord/home.html", context)


def compare(request):
    instance = (Bill.objects.values('customerId').annotate(totalSales=Sum('totalSales')).order_by())
    context = dict()
    context["companies"] = instance
    return render(request, "salesRecord/compare.html", context)
