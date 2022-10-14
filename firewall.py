# coding:utf-8


import os
from sqlite3 import Row
from tkinter import *
import tkinter
from tkinter import filedialog
from webbrowser import BackgroundBrowser
from tkinter import ttk


os.system('touch iptables.txt iptables2.txt iptables3.txt')
os.system('iptables -L INPUT --line-numbers | tee iptables.txt')
os.system('iptables -L OUTPUT --line-numbers | tee iptables2.txt')
os.system('iptables -L FORWARD --line-numbers | tee iptables3.txt')


# initialisation de l'objet fenêtre mainapp
mainapp = Tk()

""" centrage de la fenêtre par rapport à l'écran"""
largeur_ecran = mainapp.winfo_screenwidth()
hauteur_ecran = mainapp.winfo_screenheight()
largeur_fenetre = 800
hauteur_fenetre = 600

posX = int((largeur_ecran/2)-(largeur_fenetre/2))
posY = int((hauteur_ecran/2)-(hauteur_fenetre/2))

geo = "{}x{}+{}+{}".format(largeur_fenetre, hauteur_fenetre, posX, posY)
mainapp.geometry(geo)
mainapp.resizable(width=False, height=False)  # taille fenêtre non modifiable
mainapp.title("Firewall")  # nom de la fenêtre


premier_frame = tkinter.LabelFrame(
    mainapp, text="Status", width=400, height=200)  # frame pour le petit terminal
chemin = tkinter.StringVar()
chemin.set("firewall>")
chemin_label = tkinter.Label(premier_frame, textvariable=chemin)

log = tkinter.StringVar()
log.set("Firewall is presently Off")
log_label = tkinter.Label(premier_frame, textvariable=log)

chemin_label.grid(row=0, column=0)
log_label.grid(row=0, column=1)

# definition de la méthode à utiliser en cas de changements de la variable rendu
# observateur update_status

def actualiser(*args):
    Lb.delete(0, END)
    f = open("iptables.txt", "r")
    for x in f:
        Lb.insert(END, x)
    f.close()
    Lb2.delete(0, END)
    f2 = open("iptables2.txt", "r")
    for x in f2:
        Lb2.insert(END, x)
    f2.close()
    Lb3.delete(0, END)
    f3 = open("iptables3.txt", "r")
    for x in f3:
        Lb3.insert(END, x)
    f3.close()

def update_status(*args):
    if rendu.get():
        button_nvl_règle.config(state='normal')
        button_supr_regle.config(state='normal')
        log.set("the Firewall is On")
    else:
        button_supr_regle.config(state='disabled')
        button_nvl_règle.config(state='disabled')
        log.set("the firewall is Off")


def ligne_terminale():
    route = tkinter.Label(text="firewall#")
    action = tkinter.Label(textvariable=log)


# fonction au clic du boutton +
def ajout_formulaire():
    form = tkinter.Toplevel(mainapp)
    form.geometry("350x450")
    form.title("Ajout de règle")
    form.resizable(width=False, height=False)

    chaine = ""
    methode = ""
    interface = ""
    protocole = ""
    ip = ""
    port_var = ""
    ip_dest_variable = ""

    # élément du formulaire(widget)
# -A
    def tracage(event):

        if methode_A.get() == "INPUT":
            chaine = "-A INPUT"
            return chaine

        elif methode_A.get() == "OUTPUT":
            chaine = "-A OUTPUT"
            return chaine

        elif methode_A.get() == "FORWARD":
            chaine = "-A FORWARD"
            return chaine

        else:
            chaine = ""
            return chaine

# -J
    def tracage2(event):
        if methode_J.get() == "ACCEPT":
            methode = "-j ACCEPT"
            return methode

        elif methode_J.get() == "REJECT":
            methode = "-j REJECT"
            return methode

        elif methode_J.get() == "DROP":
            methode = "-j DROP"
            return methode
        elif methode_J.get() == "QUEUE":
            methode = "-j QUEUE"
            return methode
        elif methode_J.get() == "LOG":
            methode = "-j LOG"
            return methode
        else:
            methode = ""
            return methode


# -P


    def tracage4(event):
        if methode_P.get() == "TCP":
            protocole = "-p TCP"
            print("TCP")
            return protocole

        elif methode_P.get() == "UDP":
            print("UDP")
            protocole = "-p UDP"
            return protocole

        elif methode_P.get() == "SSH":
            print("SSH")
            protocole = "-p SSH"
            return protocole

        elif methode_P.get() == "SNMP":
            print("SNMP")
            protocole = "-p SNMP"
            return protocole

        elif methode_P.get() == "HTTP":
            print("HTTP")
            protocole = "-p HTTP"
            return protocole

        elif methode_P.get() == "icmp":
            print("icmp")
            protocole = "-p icmp"
            return protocole

        else:
            protocole = ""
            print("nada")
            return protocole

    def ip_traitement(*args):
        if ip_variable.get():
            ip = "-s {}".format(ip_variable.get())
            return ip

        else:
            ip = ""
            return ip

    def port_traitement(*args):
        if port.get():
            port_var = "--dport {}".format(port.get())
            return port_var
        else:
            port_var = ""
            return port_var

    def ip_traitement_destination(*args):
        if ip_destination.get():
            ip_dest_variable = "-d {}".format(ip_destination.get())
            print(ip_dest_variable)
            return ip_dest_variable
        else:
            ip_dest_variable = ""
            return ip_dest_variable

    def ajout_de_règle(*args):
        chaine2 = tracage(chaine)
        methode2 = tracage2(methode)
        protocole2 = tracage4(protocole)
        ip2 = ip_traitement(ip)
        variable_port = port_traitement(port_var)
        ip1 = ip_traitement_destination(ip_dest_variable)
        # iptables
        new_regle = "iptables {} {} {} {} {} {}".format(
            chaine2, ip2, ip1, protocole2, variable_port, methode2)
        affichage_input = "iptables -L INPUT --line-numbers | tee iptables.txt"
        affichage_output = "iptables -L OUTPUT --line-numbers | tee iptables2.txt"
        affichage_forward = "iptables -L FORWARD --line-numbers | tee iptables3.txt"

        print(new_regle)
        os.system(new_regle)
        os.system(affichage_input)
        os.system(affichage_output)
        os.system(affichage_forward)
        actualiser()
        

        # this.quit()

    # first combobox -A
    methode_liste = ["INPUT", "OUTPUT", "FORWARD"]
    methode_A = ttk.Combobox(form, values=methode_liste)
    methode_A.bind("<<ComboboxSelected>>", tracage)
    label_underscore_A = tkinter.Label(form, text="chaîne")

    # second combobox -J
    methode_liste2 = ["ACCEPT", "REJECT", "DROP", "QUEUE", "LOG"]
    methode_J = ttk.Combobox(form, values=methode_liste2)
    methode_J.bind("<<ComboboxSelected>>", tracage2)
    label_underscore_J = tkinter.Label(form, text="méthode")
    # thirds combobox --dport
    port = tkinter.StringVar()
    port.trace_variable("w", port_traitement)
    method_dport = tkinter.Entry(form, textvariable=port)
    label_underscore_dport = tkinter.Label(form, text="port")

    # input for adresse ip ohhhhh test
    # -s
    # source
    ip_variable = tkinter.StringVar()
    ip_variable.trace_variable("w", ip_traitement)
    adress_ip = tkinter.Entry(form, textvariable=ip_variable)
    label_underscore_s = tkinter.Label(form, text="IP")

    # input for adresse ip destination
    ip_destination = StringVar()
    ip_destination.trace_variable("w", ip_traitement_destination)
    ip_dest_input = tkinter.Entry(form, textvariable=ip_destination)
    ip_dest_label = tkinter.Label(form, text="IP dst")

    ip_dest_input.grid(row=7, column=4)
    ip_dest_label.grid(row=7, column=3)

    # combobox for protocolllyy
    methode_liste4 = ["TCP", "UDP", "icmp"]
    methode_P = ttk.Combobox(form, values=methode_liste4)
    methode_P.bind("<<ComboboxSelected>>", tracage4)
    label_underscore_P = tkinter.Label(form, text="protocol")

    # affichage du formulaire d'ajout de règle

    # premier comboBOx affichage chaine -A
    label_underscore_A.grid(row=0, column=3)
    methode_A.grid(row=0, column=4)
    # deuxième combo box affichage methode -j
    label_underscore_J.grid(row=2, column=3)
    methode_J.grid(row=2, column=4)

    # input de port
    label_underscore_dport.grid(row=3, column=3)
    method_dport.grid(row=3, column=4)

    # quatrième combobox affichage -p
    label_underscore_P.grid(row=5, column=3)
    methode_P.grid(row=5, column=4)

    # input de l'addresse ip affichage -s
    label_underscore_s.grid(row=6, column=3)
    adress_ip.grid(row=6, column=4)

    ajouter_règle = tkinter.Button(
        form, command=ajout_de_règle, text="ajouter une règle")
    ajouter_règle.grid(row=8, column=4)


# barre de menu
barre_de_menu_principale = tkinter.Menu(mainapp)
# élément fichier

def importation(*args):
    filename = filedialog.askopenfile()
    import_variable="iptables-restore < "
    
    
def exportation(*args):
    export_variable ="iptables-save > /etc/iptables"
    os.system(export_variable)
    
    
    
def textisation(*args):
    fichier_text_var="iptables-save > /etc/iptables.txt"
    os.system(fichier_text_var)


menu_fichier = tkinter.Menu(barre_de_menu_principale)
menu_fichier.add_command(label="Sauvegarder les règles",command=textisation)
menu_fichier.add_command(label="Importer",command=importation)
menu_fichier.add_command(label="Exporter",command=exportation)
menu_fichier.add_command(label="Quitter", command=mainapp.quit)
# élément édition

menu_edition = tkinter.Menu(barre_de_menu_principale)
menu_edition.add_command(label="Mofification")
# élément journal
menu_journal = tkinter.Menu(barre_de_menu_principale)
menu_journal.add_command(label="Voir le log")

# élément aide
menu_aide = tkinter.Menu(barre_de_menu_principale)
menu_aide.add_command(label="Utilisation")
menu_aide.add_command(label="Information sur la license")

# button d'action
button_nvl_règle = tkinter.Button(mainapp, text="+", command=ajout_formulaire)
button_nvl_règle.config(state='disabled')

# variable pour observer l'action de l'objet radio button
rendu = tkinter.IntVar()
rendu.trace_variable("w", update_status)
On = tkinter.Radiobutton(mainapp, text="On", value=1, variable=rendu)
Off = tkinter.Radiobutton(mainapp, text="Off", value=0, variable=rendu)


# tab de règles,journal,remarques
tab_initiale = ttk.Notebook(mainapp)


tab1 = ttk.Frame(tab_initiale, width=600, height=300)
tab2 = ttk.Frame(tab_initiale, width=600, height=300)
tab3 = ttk.Frame(tab_initiale, width=600, height=300)

tab_initiale.add(tab1, text="Règles")
tab_initiale.add(tab2, text="Journal")
tab_initiale.add(tab3, text="Remarques")

label_for_see = tkinter.Label(
    tab1, text="voici les règles", width=50, height=20)
label_for_see2 = tkinter.Label(
    tab2, text="voici le Journal", width=50, height=20)
label_for_see3 = tkinter.Label(
    tab3, text="voici les remarques", width=50, height=20)

# tab secondaire des règles
tab_secondaire = ttk.Notebook(tab1)

tab_règle_1 = ttk.Frame(tab_secondaire, width=600, height=300)
tab_règle_2 = ttk.Frame(tab_secondaire, width=600, height=300)
tab_règle_3 = ttk.Frame(tab_secondaire, width=600, height=300)

tab_secondaire.add(tab_règle_1, text="INPUT")
tab_secondaire.add(tab_règle_2, text="OUTPUT")
tab_secondaire.add(tab_règle_3, text="FORWARD")

# affichage tab
tab_initiale.grid(row=11, column=7)
tab_secondaire.pack()
label_for_see2.pack()
label_for_see3.pack()

# listage chaine Input
varA = int()
varB = int()
varC = int()


def getting(*args):
    line = Lb.curselection()
    item = Lb.index(ANCHOR)
    varA = item-1
    print(varA)
    return varA


def getting2(*args):
    line2 = Lb2.curselection()
    item2 = Lb2.index(ANCHOR)
    varB = item2-1
    print(varB)
    return varB


def getting3(*args):
    line3 = Lb3.curselection()
    item3 = Lb3.index(ANCHOR)
    varC = item3-1
    print(varC)
    return varC

# iptables -I INPUT 7 -s 192.168.0.1 -j REJECT \\remplacement de regles spécifique
# iptables -F INPUT \\delete all
# alaina le ligne retraretra mintsy
# atao liste liste=[str(value) for value in p.split('/n')]
# atao recherche hoe ahoana no miselectionné zavatra iray amina listbox spécifique na otranzany :)


def mine(*args):
    if (Lb.bind('<<ListboxSelect>>')):
        var_mine = getting(varA)
        print("tu fous quoi ici??")
        mamafa = "iptables -D INPUT {}".format(var_mine)
        affisy = "iptables -L INPUT --line-number | tee iptables.txt"
        os.system(mamafa)
        os.system(affisy)
    if (Lb2.bind('<<ListboxSelect>>')):
        var_mine2 = getting2(varB)
        mamafa_ny_output = "iptables -D OUTPUT {}".format(var_mine2)
        affisy2 = "iptables -L OUTPUT --line-number | tee iptables2.txt"
        os.system(mamafa_ny_output)
        os.system(affisy2)
    if(Lb3.bind('<<ListboxSelect>>')):
        var_mine3 = getting3(varC)
        mamafa_ny_forward = "iptables -D FORWARD {}".format(var_mine3)
        affisy3 = "iptables -L FORWARD --line-numbers | tee iptables3.txt"
        os.system(mamafa_ny_forward)
        os.system(affisy3)
    
    actualiser()


Lb = tkinter.Listbox(tab_règle_1, width=70, height=20, exportselection=0)
f = open("iptables.txt", "r")
for x in f:
    Lb.insert(END, x)

f.close()

Lb.bind('<<ListboxSelect>>', getting)


Lb.grid()

# listage de l'output
Lb2 = tkinter.Listbox(tab_règle_2, width=70, height=20, exportselection=0)
f2 = open("iptables2.txt", "r")
for x in f2:
    Lb2.insert(END, x)

f2.close()
Lb2.bind('<<ListboxSelect>>', getting2)

Lb2.grid()
# listage de forward
Lb3 = tkinter.Listbox(tab_règle_3, width=70, height=20, exportselection=0)
f3 = open("iptables3.txt", "r")
for x in f3:
    Lb3.insert(END, x)

f3.close()
Lb3.bind('<<ListboxSelect>>', getting3)
Lb3.grid()
# boutton up et down
bouton_up = tkinter.Button(mainapp, text="↑")
bouton_down = tkinter.Button(mainapp, text="↓")
button_supr_regle = tkinter.Button(mainapp, text="-", command=mine)
button_supr_regle.config(state='disabled')




#actualiser = tkinter.Button(mainapp, text="refresh", command=actualiser)

"""img = ImageTk.PhotoImage(Image.open("index.gif"))
panel = Label(mainapp, image = img)
panel.place(x=10,y=10)"""

# affichge boutton
bouton_down.grid(row=7, column=3)
bouton_up.grid(row=6, column=3)
#actualiser.grid(row=8, column=3)




# affichage radio et petit terminale
On.grid(row=2, column=3)
Off.grid(row=2, column=4)
premier_frame.grid(row=7, column=7)
button_nvl_règle.grid(row=3, column=4)
button_supr_regle.grid(row=3, column=5)


# affichage barre de menu et éléments
barre_de_menu_principale.add_cascade(label="Fichier", menu=menu_fichier)
barre_de_menu_principale.add_cascade(label="Edition", menu=menu_edition)
barre_de_menu_principale.add_cascade(label="Journal", menu=menu_journal)
barre_de_menu_principale.add_cascade(label="Aide", menu=menu_aide)


# affichage de la fenêtre
mainapp.config(menu=barre_de_menu_principale)
mainapp.mainloop()
