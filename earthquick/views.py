from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render
from .database import *
import ibm_db




import json

# Create your views here.

user_list = [
    {"user":"jack", "pwd":"abc"},
    {"user":"tom", "pwd":"ABC"}
]

def index(request):
    if request.method=="POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        temp = {"user":username, "pwd":password}
        print (temp)
        user_list.append(temp)
    return render(request, "index.html",{"data":user_list})

def main(request):
    if request.method=="GET":
        print (request.GET)
        if 'Longtitude' in request.GET.keys():
            longtitude = request.GET.get("Longtitude", None)
            latitude = request.GET.get("Latitude", None)
            data = {"type": "report", "longitude": longtitude, "latitude": latitude}
            return render(request, "main.html",
                          {"data":json.dumps(data)})
            #reportDamage(longtitude, latitude)
        elif 'Description' in request.GET.keys():
            resources = request.GET.getlist("resources", None)
            situation = request.GET.get("Description", None)
            water = 1 if "Water" in resources else 0
            food = 1 if "Food" in resources else 0
            clothe = 1 if "Clothe" in resources else 0
            data = {"type": "victim", "water": water, "food": food, "clothe": clothe, "situation": situation}
            return render(request, "main.html",
                          {"data": json.dumps(data)})
            #reportInjury(99, 99, water, food, clothe,  situation)
        elif 'available' in request.GET.keys():
            available = request.GET.get("available", None)
            rescuerID = request.GET.get("RescuerID", None)
            water = request.GET.get("Water", None)
            food = request.GET.get("Food", None)
            clothe = request.GET.get("Clothe", None)
            data =  {"type": "rescuer", "rescuerID": rescuerID, "water": water, "food": food, "clothe": clothe}
            return render(request, "main.html",
                          {"data": json.dumps(data)})
            #delegateDriverWork(rescuerID, food, water, clothe)
    data = {"type": "home"}
    return render(request, "main.html", {"data":json.dumps(data)})



