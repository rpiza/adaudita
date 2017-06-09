import menuClass as mc
from connecta import ad
import sys
import ldap3.core.exceptions

reports = {
"all_users": ('DC=problemeszero,DC=com','(&(samAccountName=*)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf','accountExpires','altSecurityIdentities','badPasswordTime', 'codePage','countryCode', 'homeDirectory','homeDrive','lastLogoff','lastLogon','lmPwdHistory','logonCount','mail','maxStorage',
'ntPwdHistory','otherMailbox','PasswordExpirationDate','primaryGroupID','profilePath','pwdLastSet',
'sAMAccountType','scriptPath','unicodePwd','userAccountControl','userCertificate','userSharedFolder',
'userWorkstations'],True),
"all_computers": ('DC=problemeszero,DC=com','(&(samAccountName=*)(objectClass=computer)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf'],True),
"all_groups": ('DC=problemeszero,DC=com','(&(objectClass=*)(objectCategory=CN=Group,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','member'],True)
}

def print_results(llista, json):
    #print(llista)
    for elem in llista:
        print (elem) 
   #print(adObj.c.result)
    print(json)


def establir_connexio(adObj):
    try:
        adObj.connect()
        print("Connexió establerta")
    except ldap3.core.exceptions.LDAPSocketOpenError:
        print("\nEl DC no està disponible o l'adreça/port són incorrectes")
    except ldap3.core.exceptions.LDAPBindError:
        print("\nError en l'usuari o la contrasenya!!!")
def show_connection(adObj):
    print("{0}: {1}\n{2}".format("Connexió", adObj.c,"OK"))

def menu_reports(a):
    global menu_r
    menu_r = mc.Menu(reports_choices,reports_menu)
#    global with mc.Menu(reports_choices,reports_menu) as menu_r:

    menu_r.run()

def menu_personalitzat(a):
    global menu_p
    menu_p = mc.Menu(personalitza_choices, personalitza_menu)
    menu_p.run()

def llegeix_input():
    filtre = input("Introdueix el CN de l'objecte: ")

def modify_connection():
    pass

def quit(adObj):
#    adObj.disconnect()
    try:
        print("\nDesconnectant del Directori Actiu...")
        adObj.disconnect()
    except AttributeError:
        print("No estaves connectat al Directori Actiu")
    finally:    
        print("Adéu!!!!")
        sys.exit(0)

def search(f):
    print("Cerca Oleeeee!!!!")
    f[1].get_ldap_info(f[0])
    print_results(f[1].c.response, f[1].c.response_to_json())

def enrera(a):
    global menu_r
    menu_r.seguir = False

def enrera_p(a):
    global menu_p
    menu_p.seguir = False

main_choices = {"1": [establir_connexio, ad],
"2": [show_connection, ad],
"3": [menu_reports, None],
"4": modify_connection,
"5": [quit, ad]
}

main_menu = """
          Menú:

    1. Connecta
    2. Mostra el paràmetres de la connexió
    3. Selecciona un informe
    4. Desconnecta
    5. Surt
"""
reports_choices = {
"1": [search,(reports["all_users"], ad)],
"2": [search,(reports["all_computers"], ad)],
"3": [search,(reports["all_users"], ad)],
"4": [menu_personalitzat, None],
"5": [enrera,"a"]
}

reports_menu="""
         Informes:

    1. Usuaris del domini
    2. Equips del domini
    3. Grups del domini amb usuaris/equips
    4. Cerca per Usuari/Equip/Grup
    5. Enrera
"""

personalitza_choices = {
"1": [llegeix_input,(reports["all_users"], ad)],
"2": [search,(reports["all_computers"], ad)],
"3": [search,(reports["all_users"], ad)],
"4": [menu_personalitzat, None],
"5": [enrera_p,"a"]
}

personalitza_menu="""
         Informes:

    1. Cerca per Usuari
    2. Cerca per Equip
    3. Cerca per Grup
    4. Extra
    5. Enrera
"""
