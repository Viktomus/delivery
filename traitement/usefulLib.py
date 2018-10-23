import os

def getWebAddress(request,replacement='index'):
    address = request.build_absolute_uri()

    if '%20' in address:
        address = address.replace('%20', '')
        replacement = replacement.replace(" ", '')

    temp = address.replace(replacement,'')
    return temp

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def GetHomeRedirect(request):
    isLog = GetLogState(request)
    if isLog:
        return "account"
    else:
        return "login"

def GetConnectedMsg(request):
    isLog = GetLogState(request)
    if isLog:
        return "Mon compte"
    else:
        return "Se connecter"

def SaveLogState(request, pseudo, isLog=1):
    ip = get_client_ip(request)
    f = open("databases/logstates/{0}.dat".format(ip), "w+")
    f.write("{0}={1}".format(pseudo,isLog))

def GetLogState(request):
    ip = get_client_ip(request)
    try:
        f = open("databases/logstates/{0}.dat".format(ip), "r")
    except:
        return False
    lines = f.readlines()

    for l in lines:
        value = l.split('=')[1].replace('\n', "")

        if value == "0":
            return False
        else:
            return True

def UnlogState(request):
    try:
        ip = get_client_ip(request)
        os.remove("databases/logstates/{0}.dat".format(ip))
    except:
        return

def GetPseudoFromIp(request):
    ip = get_client_ip(request)

    try:
        f = open("databases/logstates/{0}.dat".format(ip), "r")
        pseudo = f.readlines()[0].split('=')[0].replace('\n', '')
        return pseudo
    except:
        return ""

def IsPlayerAdmin(request):
    pseudo = GetPseudoFromIp(request)

    try:
        f = open("databases/users/{0}.dat".format(pseudo), "r")
        adminStr = f.readlines()[3].split('=')[1].replace('\n', '')

        if adminStr == "0":
            return False
        else:
            return True
    except:
        return False

def GetItemInfo(itemName):
    try:
        f = open("databases/items/{0}".format(itemName))
        itemInfo = ItemInfo()
        allLines = f.readlines()

        itemInfo.itemName = itemName.replace('.dat', '')
        itemInfo.price = allLines[1].split('=')[1]
        itemInfo.desc = allLines[2].split('=')[1]
        itemInfo.stock = allLines[3].split('=')[1]
        print('ok2')
        return itemInfo

    except:
        return None

def GetAllItemInfo():
    files = os.listdir("databases/items/")
    itemsInfos = list()

    for file in files:
        info = GetItemInfo(file)

        if info is not None:
            itemsInfos.append(info)
    return itemsInfos

def PrintItemInfos():
    itemsInfo = GetAllItemInfo()

    for info in itemsInfo:
        info.stringTotal = "Nom: {0}; Prix: {1}; Stock: {2}; Description: {3}".format(
            info.itemName, info.price, info.stock, info.desc)
    return itemsInfo

def GetDeliveryInfo(pseudo):
    try:
        f = open("databases/users/{0}".format(pseudo.lower()), "r")
        deliveryInfo = DeliveryInfo()
        allLines = f.readlines()
        totalLine = allLines[4].split('=')[1]

        deliveryInfo.pseudo = pseudo.replace('.dat', '')
        deliveryInfo.address = totalLine.split(';')[0]
        deliveryInfo.itemName = totalLine.split(';')[1]
        deliveryInfo.quantity = totalLine.split(';')[2]
        deliveryInfo.price = totalLine.split(';')[3]
        deliveryInfo.deliverySpeed = totalLine.split(';')[4]
        deliveryInfo.status = totalLine.split(';')[5]
        return deliveryInfo

    except:
        return None

def GetUserDeliveryInfo(pseudo):
    f = open("databases/users/{0}.dat".format(pseudo.lower()), "r")
    lines = f.readlines()
    ccLine = lines[4].replace("currentCommand=", "")
    pcLine = lines[5].replace("previousCommand=", "")
    
    data = list()

    if "null" in ccLine:
        data.append(None)
        data.append(None)
        data.append(None)

    else:
        data.append("{0} x{1}".format(ccLine.split(';')[1].capitalize(), ccLine.split(';')[2]))#nom item et quantité
        data.append(ccLine.split(';')[5])#statut
        data.append(ccLine.split(';')[3])#prix

    if "null" in pcLine:
        data.append(None)
        data.append(None)
        data.append(None)

    else:
        data.append("{0} x{1}".format(pcLine.split(';')[1].capitalize(), pcLine.split(';')[2]))
        data.append(pcLine.split(';')[5])
        data.append(pcLine.split(';')[3])

    return data

    #address;itemName;quantity;price;deliverySpeed;Commande passée;

def GetAllDeliveryInfo():
    files = os.listdir("databases/users/")
    deliveryInfos = list()

    for file in files:
        info = GetDeliveryInfo(file)

        if info is not None:
            deliveryInfos.append(info)
    return deliveryInfos

def PrintDeliveryInfos():
    deliveryInfos = GetAllDeliveryInfo()

    for info in deliveryInfos:
        info.stringTotal = "Pseudo: {0}; Addresse: {1}; Objet: {2}; Quantité: {3}; Prix: {4}; Vitesse de livraison: {5}; Statut: {6}".format(
            info.pseudo, info.address, info.itemName, info.quantity, info.price, info.deliverySpeed, info.status)
    return deliveryInfos

def ChangeToNextStep(pseudo):
    f = open("databases/users/{0}.dat".format(pseudo), "r")
    lineSteps = f.readlines()
    step = lineSteps[4].split(';')[5]

    f2 = open("databases/steps.dat", "r")
    totalLines = f2.readlines()
    newStep = ""

    i = 0

    for l in totalLines:
        if l == step + "\n":
            if i + 1 == 5:
                DeleteCommand(pseudo)
                return
            newStep = totalLines[i + 1]
            allLines = lineSteps
            allLines[4] = allLines[4].replace(step, newStep.replace('\n', ''))
            f_ = open("databases/users/{0}.dat".format(pseudo), "w")
            f_.write(''.join(allLines))
            return
        i += 1

    return

def DeleteCommand(pseudo):    
    f = open("databases/users/{0}.dat".format(pseudo), "r")
    lines = f.readlines()
    lines[5] = "previousCommand={0}\n".format(lines[4].split('=')[1])
    lines[4] = "currentCommand={0}\n".format('null')
    f = open("databases/users/{0}.dat".format(pseudo), "w")
    f.write(''.join(lines))
    return

def CreateItem(itemName, price, desc, stock, photoAddress):
    f = open("databases/items/{0}.dat".format(itemName.lower()), "w+")
    f.write("itemName={0}\n".format(itemName))
    f.write("price={0}\n".format(price))
    f.write("desc={0}\n".format(desc))
    f.write("stock={0}\n".format(stock))
    f.write("photoAddress={0}\n".format(photoAddress))
    return

def EditItemStock(itemName, stock):
    f = open("databases/items/{0}.dat".format(itemName.lower()), "r")
    lines = f.readlines()
    lines[3] = "stock={0}\n".format(stock)
    f = open("databases/items/{0}.dat".format(itemName.lower()), "w")
    f.write(''.join(lines))

def SearchItem(searchStr):
    files = os.listdir("databases/items/")
    possibleItems = list()

    for item in files:
        item = item.replace('.dat', '')

        success = False

        if (searchStr in item) or (item in searchStr):
            possibleItems.append(item)
            success = True
        else:
            success = False

        if success == False:
            nbrInCommon = 0

            for letter in item:
                if letter in searchStr:
                    nbrInCommon += 1
            if nbrInCommon >= 4:
                possibleItems.append(item)               

    return possibleItems

def SortResults(possibleItems):
    allItems = list()

    for item in possibleItems:
        lines = open("databases/items/{0}.dat".format(item), 'r').readlines()

        itemInfo = ItemInfo()

        item = item.upper()
        itemInfo.itemName = item
        itemInfo.itemNameLower = item.lower()
        itemInfo.price = lines[1].replace('price=', '')
        itemInfo.desc = lines[2].replace('desc=', '')
        itemInfo.stock = lines[3].replace('stock=', '')
        itemInfo.photoAddress = lines[4].replace('photoAddress=', '')

        stockInt = int(itemInfo.stock)

        if stockInt <= 5:
            itemInfo.stockColor = "red"
        elif stockInt <= 10:
            itemInfo.stockColor = "orange"
        else:
            itemInfo.stockColor = "green"

        allItems.append(itemInfo)

    return allItems

def GetAllItems():
    files = os.listdir("databases/items/")
    items = list()

    for file in files:
        items.append(file.replace('.dat', ''))
    return items

def SaveCommand(player, item_name, quantity, address, price):
    f = open("databases/items/{0}.dat".format(item_name), "r")
    itemLines = f.readlines()
    stock = int(itemLines[3].replace('stock=', '')) 
    quantity = int(quantity)
    if stock == 0:
        return "Cet objet est en rupture de stock ! Désolé :("
    if quantity <= 0:
        return "Pourquoi vouloir faire planter le site ?"

    f = open("databases/users/{0}.dat".format(player), "r")
    lines = f.readlines()

    if "null" in lines[4]:
        lines[4] = "currentCommand={0};{1};{2};{3};{4};{5};\n".format(address, item_name, quantity, price, 1, "Commande passée")
        f = open("databases/users/{0}.dat".format(player), "w")
        f.writelines(lines)

        f = open("databases/items/{0}.dat".format(item_name), "w")
        stock -= quantity
        itemLines[3] = "stock={0}\n".format(stock)
        f.writelines(itemLines)

        return
    else:
        return "Vous ne pouvez passer qu'une seule commande à la fois ! Attendez que la commande actuelle se termine"

def ApplyMaxStock(item_name, quantity):
    f = open("databases/items/{0}.dat".format(item_name), "r")
    itemLines = f.readlines()
    stock = int(itemLines[3].replace('stock=', ''))

    if int(quantity) > stock:
        quantity = stock

    return quantity

class DeliveryInfo:
    pseudo = ""
    address = ""
    itemName = ""
    quantity = ""
    price = ""
    deliverySpeed = ""
    status = ""
    stringTotal = ""

    def f(self):
        return None

class ItemInfo:
    itemName = ""
    itemNameLower = ""
    price = ""
    desc = ""
    stock = ""
    photoAddress = ""
    stockColor = ""
    stringTotal = ""