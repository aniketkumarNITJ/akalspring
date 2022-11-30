from django.shortcuts import render
from django.http import HttpResponse
from .models import Company


# Create your views here.
def index(request):
    allProd = Company.objects.all()
    context = {"companies": allProd}
    return render(request, "companies/home.html", context)


# getting data from form and adding it in database
def addCompany(request):
    com_name = request.POST.get("comName")
    com_addr = request.POST.get("comAdrr")
    com_cou = request.POST.get("comCountry")
    newCom = Company(company_name=com_name,company_address=com_addr,company_country=com_cou,)
    try:
        newCom.save()
    finally:
        allProd = Company.objects.all()
        context = {"companies": allProd}
        return render(request, "companies/home.html", context)


def delCompany(request):
    name = request.POST.get("name")
    try:
        Company.objects.filter(company_name=name).delete()
        return HttpResponse("Company Successfully Deleted")
    except:
        return HttpResponse("Company Failed To Deleted")


def editCompany(request):
    prev_name = request.POST.get("prev_name")
    name = request.POST.get("name")
    address = request.POST.get("address")
    country = request.POST.get("country")
    obj = Company.objects.get(company_name=prev_name)
    obj.delete()
    obj.company_name = name
    obj.company_address = address
    obj.company_country = country
    try:
        obj.save()
        return HttpResponse("Company Successfully Edited")
    except:
        return HttpResponse("Company Edition Failed same company may be present")
