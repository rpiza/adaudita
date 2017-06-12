import menuClass as mc
from connecta import ad
import sys
import readline
import ldap3.core.exceptions
import os
import random
import string

export_files = ['../exports', 'json']
tipus_ext = ('csv', 'json', 'pdf','xml')


s_base='DC=problemeszero,DC=com'
s_scope='SUBTREE'
s_attributes=['cn','memberOf','member']

filtre_consola = 'cn=admin*' #Ha de ser None

def random_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def actualitza_s_filter(t):
    ''' Crear el filtre LDAP segons el tipus d'objecte '''
    return '(&(objectClass=*)(objectCategory={f1})({f2}))'.format(
            f1 = {'u':'CN=Person,CN=Schema,CN=Configuration,{s_base}'.format(s_base=s_base),
                  'c':'CN=Computer,CN=Schema,CN=Configuration,{s_base}'.format(s_base=s_base),
                  'g':'CN=Group,CN=Schema,CN=Configuration,{s_base}'.format(s_base=s_base), 
                  '*':'*'}.get(t), 
            f2 = filtre_consola if filtre_consola else 'CN=*')

def print_results(llista, json):
    ''' Imprimiex el resultat de la consulta ldap'''
    for elem in llista:
#        if isinstance(elem,ldap3.utils.ciDict.CaseInsensitiveDict):
        if elem.get('dn'):
            print('\n\nDistinguished Name: ', elem.get('dn'))
        if isinstance(elem.get('attributes'),ldap3.utils.ciDict.CaseInsensitiveDict):
            for k, v in elem.get('attributes').items():

                if isinstance(v,list):
                    print(k,":")
                    for e in v: print ("\t", e)
#            print ("memberOf: ", elem.get('attributes').get('memberOf'))


#        print (elem) 
#    print(ad.c.result)
#    print(llista)
#    print(json)

def export_json():
    return ad.c.response_to_json()

def export_csv():
    pass

def export_pdf():
    pass

def export_xml():
    pass

def menu_reports(a):
    ''' Crea el menu del informes'''
    global menu_r
    menu_r = mc.Menu(reports_choices,reports_menu)
    menu_r.run()

def menu_personalitzat(a):
    '''Crea el menu de les cerques personalitzades'''
    global menu_p
    menu_p = mc.Menu(personalitza_choices, personalitza_menu)
    menu_p.run()

def menu_export(a):
    '''Crea el menu dels parametres d'exportació'''
    global menu_e
    menu_e = mc.Menu(export_choices, export_menu)
    veure_params(0)
    menu_e.run()

def establir_connexio(adObj):
    ''' Estableix la connexio al DC'''
    try:
        adObj.connect()
        print("Connexió establerta")
    except ldap3.core.exceptions.LDAPSocketOpenError:
        print("\nEl DC no està disponible o l'adreça/port són incorrectes")
    except ldap3.core.exceptions.LDAPBindError:
        print("\nError en l'usuari o la contrasenya!!!")

def show_connection(adObj):
    '''Mostra les dades de la connexio actual'''
    print("{0}: {1}\n{2}".format("Connexió", adObj.c,"OK"))

def modify_connection():
    pass

def search(f):
    '''Composicio del filtre de cerca ldap, executa la cerca i crida la funcio per imprimir els resultats'''
    data = (s_base, actualitza_s_filter(f[0]), s_scope, s_attributes, False)
    print ("\nFiltre de cerca", data, "\n", s_attributes)
#    return None
    global filtre_consola 
    filtre_consola = None
#   Execucio de la cerca al ldap
    try:
        f[1].get_ldap_info(data)
    except ldap3.core.exceptions.LDAPInvalidFilterError:
        print("\nEi!!!! Hi ha un error en el filtre!!!")
        return
    except AttributeError:
        print("\nEi!!!! Comprova que has establert la connexió al DC!!!")  
        return  
    print_results(f[1].c.response, f[1].c.response_to_json())

def llegeix_input(f):
    global filtre_consola
    print ('''Exemples de filtres de cerca:
            cn=admin*
            &(GivenName=John)(SN=Doe)
            |(GivenName=John)(GivenName=Joe)''')
    filtre_consola = input("Introdueix el filtre ldap de la cerca: ")
    search(f)

def modifica_param(f):
    c = None
    global export_files
    export_files[f] = input("Introdueix el nou valor: ")

    if not os.path.exists(export_files[f]) and (f == 0):
        while c not in ['s','S', 'n', 'N','' ]:        
            c = input("El directori introduit no existeix. El vols crear[s/N]: ")
        if c in ['s','S']: os.makedirs(export_files[f])

    if (export_files[f] not in tipus_ext) and (f == 1): 
        print('Els tipus d\'extensió possibles són:', tipus_ext)
        while c not in tipus_ext:        
            c = input('Tria un tipus de fitxer dels possibles. L\'extensió NO ha de incloure les \': ')
        export_files[f] = c

def veure_params(a):
    print('\n\tDades d\'exportació actuals:\n\t\t- Ruta: {f1}\n\t\t- Extensió: {f2}\n'.format(
        f1 = export_files[0], f2 = export_files[1]))

def result_export(a):
    '''Genera un fitxer amb els resultats de la darrera consulta'''

    nom_f = random_generator()
    nom_f_1 = input("\n\tNom del fitxer [{nom}]: ".format(nom = nom_f))
    if nom_f_1: nom_f = nom_f_1

    print('\n\tEl resultat es guardarà a ', export_files[0] + '/' + nom_f + '.' + export_files[1])

    try:
        f = open(export_files[0] + '/' + nom_f + '.' + export_files[1], 'w')
        f.write({'json': export_json,'csv': export_csv,'pdf': export_pdf,'xml': export_xml}.get(export_files[1])())
        f.close()
    except: 
        return

def enrera(a):
    global menu_r
    menu_r.seguir = False

def enrera_p(a):
    global menu_p
    menu_p.seguir = False

def enrera_e(a):
    global menu_e
    menu_e.seguir = False

def quit(adObj):
    try:
        print("\nDesconnectant del Directori Actiu...")
        adObj.disconnect()
    except AttributeError:
        print("No estaves connectat al Directori Actiu")
    finally:    
        print("Adéu!!!!")
        sys.exit(0)

main_choices = {"3": [establir_connexio, ad],
"2": [show_connection, ad],
"1": [menu_reports, None],
"4": [modify_connection, None],
"5": [quit, ad]
}

main_menu = """
          Menú:

    1. Selecciona un informe
    2. Mostra el paràmetres de la connexió
    3. Connecta al ldap
    4. Desconnecta del ldap
    5. Surt de l'aplicació
"""
reports_choices = {
"1": [search,('u', ad)],
"2": [search,('c', ad)],
"3": [search,('g', ad)],
"4": [menu_personalitzat, None],
"5": [result_export, None],
"6": [menu_export, None],
"7": [enrera, None]
}

reports_menu="""
         Informes:

    1. Usuaris del domini
    2. Equips del domini
    3. Grups del domini amb usuaris/equips
    4. Cerca personalitzada per Usuari/Equip/Grup
    5. Exporta el resultat
    6. Paràmetres exportació fitxers
    7. Enrera
"""

personalitza_choices = {
"1": [llegeix_input,('u', ad)],
"2": [llegeix_input,('c', ad)],
"3": [llegeix_input,('g', ad)],
"4": [llegeix_input,('*', ad)],
"5": [enrera_p, None]
}

personalitza_menu="""
         Informes 2:

    1. Cerca per Usuari
    2. Cerca per Equip
    3. Cerca per Grup
    4. Cerca qualsevol objecte
    5. Enrera
"""
export_choices = {
"1": [modifica_param, 0],
"2": [modifica_param, 1],
"3": [veure_params, 0],
"4": [enrera_e, None]
}

export_menu="""
         Modifica paràmetres exportació:

    1. Modifca ruta
    2. Modifica extensió
    3. Veure els paràmetres
    4. Enrera
"""


