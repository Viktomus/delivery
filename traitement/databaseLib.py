
def RegisterClient(pseudo, password, email):
    try:
        open("databases/users/{0}.dat".format(pseudo.lower()), "r")
        return True, "Ce pseudo est déjà utilisé !"
    except:
        if IsEmailUsed(email, pseudo):
            return True, "Cette addresse mail est déjà utilisée !"

        f = open("databases/users/{0}.dat".format(pseudo.lower()), "w+")

        f.write("pseudo={0}\n".format(pseudo.lower()))
        f.write("password={0}\n".format(password))
        f.write("email={0}\n".format(email.lower()))
        f.write("admin=0\n")
        f.write("currentCommand=null\n")
        f.write("previousCommand=null\n")
        return False, ""

def LoginClient(pseudo, password):
    try:
        f = open("databases/users/{0}.dat".format(pseudo.lower()), "r")
        lines = f.readlines()
        passwordLine = lines[1].replace("password=", "")

        if passwordLine == password + "\n":
            return False
        else:
            return True
    except:
        return True

def IsEmailUsed(email, pseudo):
    f = open("databases/emails.db", "r")
    lines = f.readlines()

    for l in lines:
        if l.replace("\n", "") == email.lower():
            return True

    try:
        open("databases/users/{0}.dat".format(pseudo.lower()), "r")   
        f = open("databases/emails.db", "a")
        f.write("{0}\n".format(email.lower()))
        return False
    except:
        return True