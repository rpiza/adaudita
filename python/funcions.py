import menuClass as mc
from connecta import ad
import sys
#import readline
import ldap3.core.exceptions
import os
import random
import string
import webbrowser
import tempfile
import time
import settings
from exports import print_results, export_html, export_json, export_csv, export_pdf, export_xml

export_files = ['./exports', 'html']
tipus_ext = ('csv', 'json', 'pdf', 'xml', 'html')


filtre_consola = None # 'cn=admin*' #Ha de ser None

def random_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def actualitza_s_filter(t):
    ''' Crear el filtre LDAP segons el tipus d'objecte '''
    return '(&(objectClass=*)(objectCategory={f1})({f2}))'.format(
            f1 = {'u':'CN=Person,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                  'c':'CN=Computer,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                  'g':'CN=Group,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base), 
                  '*':'*'}.get(t), 
            f2 = filtre_consola if filtre_consola else 'CN=*')


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

def menu_atributs(a):
    '''Crea el menu per modificar els atributs de la consulta'''
    global menu_a
    menu_a = mc.Menu(atributs_choices, atributs_menu)
    veure_atributs(0)
    menu_a.run()

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
    c=None
    data = (settings.search_fields.base, actualitza_s_filter(f[0]), settings.search_fields.scope, settings.search_fields.attributes, False)
    print ("\n\nFiltre de cerca: ", data, "\n\nAtributs retornats: ", settings.search_fields.attributes, "\n")
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
    #Mostrar el fitxer per pantalla o guardar a un fitxer
    while c not in ['p','P', 'W', 'w','' ]:        
        c = input("Vols veure els resultats al navegador web o per pantalla: [W/p] ")
    if c in ['p','P']:   
        print_results(f[1].c.response, f[1].c.response_to_json())
    else:
        result_open_html() 

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

def result_export(adObj):
    '''Genera un fitxer amb els resultats de la darrera consulta'''
    c = None

    if not os.path.exists(export_files[0]):
        print ('\nEl directori d\'exportació: \'{f1}\', no existeix!!!\nRevisa els paràmetres d\'exportació de fitxers'.format(
            f1=export_files[0]))
        return
    
    #Generam un nom de fitxer aleatori
    nom_f = random_generator()
    nom_f_1 = input("\n\tNom del fitxer [{nom}]: ".format(nom = nom_f))
    if nom_f_1: nom_f = nom_f_1
    
    print('\n\tEl resultat es guardarà a ', export_files[0] + '/' + nom_f + '.' + export_files[1])
    
    try:
        f = open(export_files[0] + '/' + nom_f + '.' + export_files[1], 'w')
        f.write({'json': export_json,'csv': export_csv,'pdf': export_pdf,'xml': export_xml,'html': export_html}.get(
            export_files[1])(adObj))
        f.close()
    
        while c not in ['s','S', 'n', 'N','' ]:        
            c = input('\n\tVols obrir el fitxer [s/N]: ')
        if c in ['s','S']: webbrowser.open(export_files[0] + '/' + nom_f + '.' + export_files[1])
    
    except:
        print ("Unexpected error:", sys.exc_info()[0]) 
        return

def result_open_html():
    '''Obri el resultats de la darrera consulta a l'aplicacio html'''
    
    try:
        fp = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        fp.write(str.encode(export_html(ad)))
        fp.seek(0)
        webbrowser.open(fp.name)
    
    except:
        print ("Unexpected error:", sys.exc_info()[0]) 
        return

def modifica_atributs(f):
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

def veure_atributs(a):
    print('\n\tAtributs: {f1}'.format(
        f1 = settings.search_fields.attributes))

def enrera(a):
    global menu_r
    menu_r.seguir = False

def enrera_p(a):
    global menu_p
    menu_p.seguir = False

def enrera_e(a):
    global menu_e
    menu_e.seguir = False

def enrera_a(a):
    global menu_a
    menu_a.seguir = False

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
===================================================================================================
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
"5": [menu_atributs, None],
"6": [result_export, ad],
"7": [menu_export, None],
"8": [enrera, None]
}

reports_menu="""
===================================================================================================
         Informes:

    1. Usuaris del domini
    2. Equips del domini
    3. Grups del domini amb usuaris/equips
    4. Cerca personalitzada per Usuari/Equip/Grup
    5. Atributs de sortida
    6. Exporta el resultat
    7. Paràmetres exportació fitxers
    8. Enrera
"""

personalitza_choices = {
"1": [llegeix_input,('u', ad)],
"2": [llegeix_input,('c', ad)],
"3": [llegeix_input,('g', ad)],
"4": [llegeix_input,('*', ad)],
"5": [enrera_p, None]
}

personalitza_menu="""
===================================================================================================
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
===================================================================================================
         Modifica paràmetres exportació:

    1. Modifica ruta
    2. Modifica extensió
    3. Veure els paràmetres
    4. Enrera
"""

atributs_choices = {
"1": [veure_atributs, 0],
"2": [modifica_atributs, 1],
"3": [veure_atributs, 0],
"4": [enrera_a, None]
}

atributs_menu="""
===================================================================================================
         Modifica els atributs de les consultes:

    1. Veure atributs
    2. Modifica atributs
    3. Extra
    4. Enrera
"""

