import menuClass as mc
from connecta import ad
import sys
import ldap3.core.exceptions

s_base='DC=problemeszero,DC=com'
s_scope='SUBTREE'
s_attributes=['cn','member']

filtre_consola = 'cn=admin*' #Ha de ser None

def actualitza_s_filter(t):
    ''' Crear el filtre LDAP segons el tipus d'objecte '''
   
    return {'u':'(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,{s_base})({f2}))'.format(s_base=s_base,f2 = filtre_consola if filtre_consola else 'samAccountName=*'), 'c': '(&(objectClass=*)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,{s_base})({f2}))'.format(s_base=s_base,f2 = filtre_consola if filtre_consola else 'samAccountName=*'),'g':'(&(objectClass=*)(objectCategory=CN=Group,CN=Schema,CN=Configuration,{s_base})({f2}))'.format(s_base=s_base, f2 = filtre_consola if filtre_consola else 'samAccountName=*'),'*':'(&(objectClass=*)({f2}))'.format(s_base=s_base, f2 = filtre_consola if filtre_consola else 'samAccountName=*')}.get(t)


def print_results(llista, json):
    #print(llista)
    for elem in llista:
        print (elem) 
   #print(adObj.c.result)
    print(json)

def establir_connexio(adObj):
    ''' Establix la connexio al DC'''
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
    menu_r.run()

def menu_personalitzat(a):
    global menu_p
    menu_p = mc.Menu(personalitza_choices, personalitza_menu)
    menu_p.run()

def llegeix_input(f):
    global filtre_consola
    filtre_consola = input("Introdueix l'objecte que vols cercar: ")
    search(f)

def modify_connection():
    pass

def quit(adObj):
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
    #Composicio del filtre per a la cerca
    data = (s_base, actualitza_s_filter(f[0]), s_scope, s_attributes, True)
#    print (data)
#    return None
    global filtre_consola 
    filtre_consola = None

    f[1].get_ldap_info(data)
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
"1": [search,('u', ad)],
"2": [search,('c', ad)],
"3": [search,('g', ad)],
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
"1": [llegeix_input,('u', ad)],
"2": [llegeix_input,('c', ad)],
"3": [llegeix_input,('g', ad)],
"4": [llegeix_input,('*', ad)],
"5": [enrera_p,"a"]
}

personalitza_menu="""
         Informes 2:

    1. Cerca per Usuari
    2. Cerca per Equip
    3. Cerca per Grup
    4. Cerca qualsevol objecte
    5. Enrera
"""
