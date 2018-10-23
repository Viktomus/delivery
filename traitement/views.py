from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .databaseLib import *
from .usefulLib import *

import sys

loginErrorMsg = "Le pseudo ou le mot de passe est incorrect !"
registerPasswordError = "Les mots de passe ne correspondent pas !"

def home(request):
    if(request.method == 'POST'):
        form = HomeForm(request.POST)

        if(form.is_valid()):
            search = form.cleaned_data['search']
            results = SearchItem(search)
            return render(request, "home.html", {"form": form, "webaddress": getWebAddress(request), "results": SortResults(results), "isConnected": GetConnectedMsg(request), "logredirect": GetHomeRedirect(request)})
    else:
        form = HomeForm()
    return render(request, "home.html", {"form": form, "webaddress": getWebAddress(request), "isConnected": GetConnectedMsg(request), "logredirect": GetHomeRedirect(request), 'allItems': SortResults(GetAllItems())})

def login(request):
    if(request.method == 'POST'):
        form = LoginForm(request.POST)

        if(form.is_valid()):
            pseudo = form.cleaned_data['nom']
            pswd = form.cleaned_data['mdp']
            hasError = LoginClient(pseudo, pswd)

            if(hasError):
                return render(request, "login.html", {"form": form, "webaddress": getWebAddress(request, "login"), "error": loginErrorMsg})
            else:
                SaveLogState(request, pseudo)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "webaddress": getWebAddress(request, "login")})

def register(request):
    if(request.method == 'POST'):
        form = RegisterForm(request.POST)

        if(form.is_valid()):
            pseudo = form.cleaned_data['pseudo']
            pswd = form.cleaned_data['password']
            pswdCfrm = form.cleaned_data['passwordCfrm']
            email = form.cleaned_data['mail']

            if(pswd != pswdCfrm):
                return render(request, "register.html", {"form": form, "webaddress": getWebAddress(request, "register"), "error": registerPasswordError}) 

            hasError, msg = RegisterClient(pseudo, pswd, email)

            if(hasError):
                return render(request, "register.html", {"form": form, "webaddress": getWebAddress(request, "register"), "error": msg}) 
            else:
                SaveLogState(request, pseudo)
                return redirect('/')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form, "webaddress": getWebAddress(request, "register")})

def checkout(request, item_name, quantity):
    if GetLogState(request) == False:
        return redirect('/')
    newQuantity = ApplyMaxStock(item_name, quantity)
    price = open("databases/items/{0}.dat".format(item_name), "r").readlines()[1].replace('price=', '')
    totalPrice = int(newQuantity) * int(price)
    totalPrice = totalPrice + totalPrice * (3/100)

    if(request.method == 'POST'):
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            GPSAddress = form.cleaned_data['GPSAddress']
            result = SaveCommand(GetPseudoFromIp(request), item_name, newQuantity, GPSAddress, totalPrice)

            if result is not None:
                return render(request, "checkout.html", {"form": form, "webaddress": getWebAddress(request, "checkout/{0}/{1}".format(item_name, quantity)), "t_price": totalPrice, "item_name": "{0} x{1}".format(item_name.title(), newQuantity), "price": int(newQuantity) * int(price), 'error': result})

            else:
                return redirect('/')

    else:
        form = CheckoutForm()
    return render(request, "checkout.html", {"form": form, "webaddress": getWebAddress(request, "checkout/{0}/{1}".format(item_name, quantity)), "t_price": totalPrice, "item_name": "{0} x{1}".format(item_name.title(), newQuantity), "price": int(newQuantity) * int(price)})

def account(request):    
    if IsPlayerAdmin(request):
        if request.method == 'POST':
            UnlogState(request)
            return redirect('/')

        return render(request, "account_admin.html", {"webaddress": getWebAddress(request, "account"), "commands": PrintDeliveryInfos()})
    else:
        if request.method == 'POST':
            UnlogState(request)
            return redirect('/')

        dataList = GetUserDeliveryInfo(GetPseudoFromIp(request))
        return render(request, "account_user.html", {"webaddress": getWebAddress(request, "account"), 
        "objects_c": dataList[0], "cmdStatus_c": dataList[1], "t_price_c": dataList[2], 
        "objects": dataList[3], "cmdStatus": dataList[4], "t_price": dataList[5]})

def nextStep(request, pseudo):
    ChangeToNextStep(pseudo)
    return redirect('/account')

def createItem(request):
    if IsPlayerAdmin(request):
        if request.method == 'POST':
            form = ItemCreationForm(request.POST)

            if form.is_valid():
                itemName = form.cleaned_data['itemName']
                price = form.cleaned_data['price']
                desc = form.cleaned_data['desc']
                stock = form.cleaned_data['stock']
                photoAddress = form.cleaned_data['photoAddress']
                CreateItem(itemName, price, desc, stock, photoAddress)
                return redirect('/')

        else:
            form = ItemCreationForm()
        return render(request, "create_item.html", {"webaddress": getWebAddress(request, "createItem"), "form": form})
    else:
        return redirect('/')

def confirmEdit(request, item_name, new_stock):
    if IsPlayerAdmin(request):
        EditItemStock(item_name, new_stock)
    return redirect('/')

def listItems(request):
    if IsPlayerAdmin(request):
        return render(request, "list_items.html", {"webaddress": getWebAddress(request, "listItems"), "items": PrintItemInfos()})
    else:
        return redirect('/')

def deleteItem(request, item_name):
    os.remove("databases/items/{0}.dat".format(item_name))
    return redirect('/listItems')