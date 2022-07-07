import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cProfile import label
from tkinter import *
from tkinter import filedialog
from pathlib import Path
import os
import math
from base64 import b64decode, b64encode
import configparser
import time

current_version = "v1.0"


# Load config file or create a new one

if not os.path.isfile("config.txt"):
    print("Creating new config file...")
    with open('config.txt', 'w') as f:
        new_config = configparser.ConfigParser()
        new_config["config"]={"GUIScale":1,"BackgroundColor":"#6179C0","ForegroundColor":"#FAFFD5","FontColor":"#000000","Font":"OpenSans","FontSize":12}
        new_config.write(f)
config = configparser.ConfigParser()
config.read("config.txt")

# Create and configure the root application gui
root = Tk()

root.geometry(str(math.floor(float(config["config"]["GUIScale"]) * 720)) + "x" + str(math.floor(float(config["config"]["GuiScale"]) * 720)))
root.resizable(0,0)
root.configure(bg="#6179C0")
root.title("OpenPasswordManager " + current_version + " by Nick Tonjum")

# Create directory file
if not os.path.isfile("directory.lib"):
    print("Creating new directory file...")
    with open('directory.lib', 'w') as f:
        f.write("{}")

directory = eval(open('directory.lib',"r").read())
print(directory)


objects = []


vaultoptionvar = StringVar()
vaultoptionvar.set("")

def ConformToScale(number):
    return math.floor(float(config["config"]["GUIScale"]) * number)


newvaultnamevar = StringVar()
newvaultpasswordvar = StringVar()
newvaultconfirmpasswordvar = StringVar()
newvaultlocationvar = StringVar()
newpasswordstrength = StringVar()
newpasswordstrength.set("")
newvaultnamevar.set("")
newvaultpasswordvar.set("")
newvaultconfirmpasswordvar.set("")
newvaultlocationvar.set("")

createbuttonsmuggler = []
confirmationsmuggler = []

def Clear():
    global createbuttonsmuggler,confirmationsmuggler
    for object in objects:
        object.destroy()
    newvaultnamevar.set("")
    newvaultpasswordvar.set("")
    newvaultconfirmpasswordvar.set("")
    newvaultlocationvar.set("")
    createbuttonsmuggler = []
    confirmationsmuggler = []



def MainPage():
    global objects,vaultoptionvar,newvaultnamevar,newvaultpasswordvar,newvaultconfirmpasswordvar,newvaultlocationvar
    Clear()
    vaulttext = Label(text="Vault:",bg=config["config"]["backgroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaulttext.place(x=ConformToScale(10),y=ConformToScale(15))
    vaultkeys = []
    for i in directory.keys():
        vaultkeys.append(i)
    vaultkeys.sort()
    vaultoptions = vaultkeys + ["...Import Vault","...Create Vault"]
    vaultdropdown = OptionMenu(root,vaultoptionvar,*vaultoptions)
    vaultdropdown.config(bg=config["config"]["foregroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultdropdown["menu"].config(bg=config["config"]["foregroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultdropdown.place(x=ConformToScale(70),y=ConformToScale(10))

    objects.append(vaulttext)
    objects.append(vaultdropdown)


def EstimatePasswordStrength(foo,bar,ntmedia):
    password = newvaultpasswordvar.get()
    points = 0
    if len(password) >= 8:
        points += 2
    if len(password) >= 12:
        points += 2
    letters = set(password)
    mixed = any(letter.islower() for letter in letters) and any(letter.isupper() for letter in letters)
    if mixed:
        points +=2
    special_characters = "!@#$%^&*()-+?_=,<>/"
    if any(c in special_characters for c in password):
        points +=2
    digitlist = "1234567890"
    if any(c in digitlist for c in password):
        points +=2

    if points == 0:
        newpasswordstrength.set("Very Weak (0/10)")
    if points == 2:
        newpasswordstrength.set("Weak (2/10)")
    if points == 4:
        newpasswordstrength.set("Fair (4/10)")
    if points == 6:
        newpasswordstrength.set("Good (6/10)")
    if points == 8:
        newpasswordstrength.set("Great (8/10)")
    if points == 10:
        newpasswordstrength.set("Very Strong (10/10)")


newvaultpasswordvar.trace("w",EstimatePasswordStrength)

def SelectNewVaultLocation():
    selectedfolder = filedialog.askdirectory()
    newvaultlocationvar.set(str(Path(selectedfolder)))

def CreateVault():
    name = newvaultnamevar.get()
    password = str(newvaultpasswordvar.get()).encode('ascii')
    location = newvaultlocationvar.get()
    directory[name] = location
    vaultfile = Path(location) / str(name+".opmv")
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,iterations=390000,salt=b'openpasswordmanagerbynicktonjum')
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fernkey = Fernet(key)
    with open(vaultfile,"wb") as f:
        f.write(fernkey.encrypt("{}".encode('ascii')))
        f.close()
    MainPage()


def CreateVaultPage():
    global objects, confirmationsmuggler, newpasswordstrength, createbuttonsmuggler
    Clear()
    newpasswordstrength.set("")
    vaultnametext = Label(text="Vault Name:",bg=config["config"]["backgroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultnametext.place(x=ConformToScale(85),y=ConformToScale(250))
    vaultpasswordtext = Label(text="Password:",bg=config["config"]["backgroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultpasswordtext.place(x=ConformToScale(85),y=ConformToScale(300))
    vaultconfirmpasswordtext = Label(text="Confirm Password:",bg=config["config"]["backgroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultconfirmpasswordtext.place(x=ConformToScale(85),y=ConformToScale(350))
    vaultlocationtext = Label(text="Location:",bg=config["config"]["backgroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultlocationtext.place(x=ConformToScale(85),y=ConformToScale(400))

    vaultnameentry = Entry(root,textvariable=newvaultnamevar,bg=config["config"]["foregroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultnameentry.place(x=ConformToScale(285),y=ConformToScale(250))
    vaultpasswordentry = Entry(root,show="*",textvariable=newvaultpasswordvar,bg=config["config"]["foregroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultpasswordentry.place(x=ConformToScale(285),y=ConformToScale(300))
    vaultconfirmpasswordentry = Entry(root,show="*",textvariable=newvaultconfirmpasswordvar,bg=config["config"]["foregroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultconfirmpasswordentry.place(x=ConformToScale(285),y=ConformToScale(350))
    confirmationsmuggler.append(vaultconfirmpasswordentry)
    vaultselectlocation = Button(text="Select",width=6,height=1,bg=config["config"]["foregroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]),command=lambda: SelectNewVaultLocation())
    vaultselectlocation.place(x=ConformToScale(520),y=ConformToScale(396))
    vaultlocationentry = Entry(root,state=DISABLED,textvariable=newvaultlocationvar,bg=config["config"]["foregroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    vaultlocationentry.place(x=ConformToScale(285),y=ConformToScale(400))
    passstrengthmeter = Label(textvariable=newpasswordstrength,bg=config["config"]["backgroundcolor"],fg=config["config"]["fontcolor"],font=(config["config"]["font"],config["config"]["fontsize"]))
    passstrengthmeter.place(x=ConformToScale(515),y=ConformToScale(300))

    createbutton = Button(state=DISABLED,text="Create",width=ConformToScale(10),height=ConformToScale(2),bg="#65FF60",fg="#000000",font=(config["config"]["font"],config["config"]["fontsize"]),command=lambda:CreateVault())
    createbutton.place(x=ConformToScale(200),y=ConformToScale(500))
    createbuttonsmuggler.append(createbutton)
    cancelbutton = Button(text="Cancel",width=ConformToScale(10),height=ConformToScale(2),bg="#FF6060",fg="#000000",font=(config["config"]["font"],config["config"]["fontsize"]),command=lambda:MainPage())
    cancelbutton.place(x=ConformToScale(350),y=ConformToScale(500))

    objects.append(vaultnameentry)
    objects.append(vaultpasswordentry)
    objects.append(vaultconfirmpasswordentry)
    objects.append(vaultselectlocation)
    objects.append(vaultlocationentry)
    objects.append(passstrengthmeter)
    objects.append(createbutton)
    objects.append(cancelbutton)
    objects.append(vaultnametext)
    objects.append(vaultpasswordtext)
    objects.append(vaultconfirmpasswordtext)
    objects.append(vaultlocationtext)

def ImportVaultPage():
    Clear()



MainPage()

newvaultconfirm = 0

while True:
    root.update()
    root.update_idletasks
    if vaultoptionvar.get() == "...Create Vault":
        CreateVaultPage()
        vaultoptionvar.set("")
    if vaultoptionvar.get() == "...Import Vault":
        ImportVaultPage()
        vaultoptionvar.set("")

    if not newvaultconfirmpasswordvar.get() == "":
        if newvaultpasswordvar.get() == newvaultconfirmpasswordvar.get():
            for confirmationbox in confirmationsmuggler:
                confirmationbox.config(bg="#65FF60")
                newvaultconfirm = 1
        else:
            for confirmationbox in confirmationsmuggler:
               confirmationbox.config(bg="#FF6060")
               newvaultconfirm = 0
        
        okaytocreate = 0
        if not newvaultnamevar.get() == "":
            if not newvaultpasswordvar.get() == "":
                if not newvaultconfirmpasswordvar.get() == "":
                    if not newvaultlocationvar.get() == "":
                        if newvaultconfirm == 1:
                            for createbutton in createbuttonsmuggler:
                                okaytocreate = 1
        if okaytocreate == 1:
            createbutton.config(state=NORMAL)

