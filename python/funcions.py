import menuClass as mc
from connecta import ad
import sys

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
    adObj.connect()
    print("Connexió establerta")


def show_connection(adObj):
    print("{0}: {1}\n{2}".format("Connexió", adObj.c,"OK"))

def menu_reports(a):
    global menu_r
    menu_r = mc.Menu(reports_choices,reports_menu)
#    global with mc.Menu(reports_choices,reports_menu) as menu_r:

    menu_r.run()

def modify_connection():
    pass

def quit(adObj):
    print("Adéu!!!!")
    adObj.disconnect()
    sys.exit(0)

def search(f):
    print("Cerca Oleeeee!!!!")
    f[1].get_ldap_info(f[0])
    print_results(f[1].c.response, f[1].c.response_to_json())

def enrera(a):
    global menu_r
    menu_r.seguir = False

main_choices = {"1": [establir_connexio, ad],
"2": [show_connection, ad],
"3": [menu_reports, None],
"4": modify_connection,
"5": [quit, ad]
}

main_menu = """
Menú
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
"4": [search,(reports["all_users"], ad)],
"5": [enrera,"a"]
}

reports_menu="""
Informes:
1. Usuaris del domini
2. Equips del domini
3. Grups del domini amb usuaris/equips
4. Extra
5. Enrera
"""
