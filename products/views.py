from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


# Create your views here.
def index(request):
    allProd = Product.objects.all()
    context = {"products": allProd}
    return render(request, "products/home.html", context)


# getting data from form and adding it in database
def addProduct(request):
    newProd = Product(product_name=request.POST.get("productName"),
                      hsnCode=request.POST.get("hsnCode"), weight=request.POST.get("weight"))
    try:
        newProd.save()
    finally:
        allProd = Product.objects.all()
        context = {"products": allProd}
        return render(request, "products/home.html", context)


def delProduct(request):
    name = request.POST.get("name")
    try:
        Product.objects.filter(product_name=name).delete()
        return HttpResponse("Product Successfully Deleted")
    except:
        return HttpResponse("Product Deletion Failed")


def editProduct(request):
    prev_name = request.POST.get("prev_name")
    name = request.POST.get("name")
    code = request.POST.get("hsnCode")
    weight = request.POST.get("weight")
    obj = Product.objects.get(product_name=prev_name)
    obj.delete()
    obj1 = Product(product_name=name, hsnCode=code, weight=weight)

    try:
        obj1.save()
        return HttpResponse("Product Successfully Edited")
    except:
        return HttpResponse("Failed you may have named product to some other product")
