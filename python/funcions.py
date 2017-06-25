#import menuClass as mc
from connecta import ad, establir_connexio, show_connection, modify_connection, search_ad
import settings
from settings import menus
from exports import print_results, export_html, export_json, export_csv, export_pdf, result_open_html

import sys
import readline
'''La funcio del modul readline es manternir history de les comandes executades. 
    Amb windows no he conseguit carregar aquest modul.
    Es pot comentar. No afecta al funcionamen del programa'''
import os
import random
import string
import time
import webbrowser
import ast

export_files = ['./exports', 'csv']
tipus_ext = ('csv', 'json', 'pdf', 'html')

#Cream les variables dels objectes Menu()
global menus
#menus = {'m_reports': None, 'm_personalitzat': None, 'm_atributs': None, 'm_export': None, 'm_informes': None}

#for menu in menus.keys():
#    menus[menu] = mc.Menu()
###Then you can reference them with:
##menus['m_personalitzat'].temperature()

def random_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def crear_menu(m):
    '''Funcio que inicialitza un objtecte Menu()'''
    m[0].__init__(m[1],m[2])
    m[0].run()

def search(f):
    ''' executa la funcio de search_ad i crida la funcio per imprimir els resultats'''

    adObj = search_ad(f)

    c = None
    while c not in ['p','P', 'W', 'w','' ]:        
        c = input("Vols veure els resultats al navegador web o per pantalla: [W/p] ")
    if c in ['p','P']:   
        print_results(adObj.c.response, adObj.c.response_to_json())
    else:
        result_open_html(adObj) 

#def search_v2(f):
#    ''' executa la funcio de search_ad_v2 i crida la funcio per imprimir els resultats'''

#    adObj = search_ad_v2(f)

#    c = None
#    while c not in ['p','P', 'W', 'w','' ]:        
#        c = input("Vols veure els resultats al navegador web o per pantalla: [W/p] ")
#    if c in ['p','P']:   
#        print_results(adObj.c.response, adObj.c.response_to_json())
#    else:
#        result_open_html(adObj) 

def llegeix_input(f):

    print ('''Exemples de filtres de cerca:
            cn=admin*
            &(GivenName=John)(SN=Doe)
            |(GivenName=John)(GivenName=Joe)''')
    settings.filtre_consola = input("Introdueix el filtre ldap de la cerca: ")
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
    
#try:
    f = open(export_files[0] + '/' + nom_f + '.' + export_files[1], 'w')
    f.write({'json': export_json,'csv': export_csv,'pdf': export_pdf, 'html': export_html}.get(
        export_files[1])(adObj))
    f.close()

    while c not in ['s','S', 'n', 'N','' ]:        
        c = input('\n\tVols obrir el fitxer [s/N]: ')
    if c in ['s','S']: webbrowser.open(export_files[0] + '/' + nom_f + '.' + export_files[1])

#except:
#    print ("Unexpected error:", sys.exc_info()[0]) 
#    return

def intro_atributs(a):
    settings.search_fields = settings.search_fields._replace( attributes = ast.literal_eval( "[" + input(
                          'Introdueix el atributs entre \' i separats per ,\nExemple: \'cn\',\'memberOf\' :') + "]"))

def mod_atributs(a):
    settings.search_fields = settings.search_fields._replace(attributes={'a': settings.attr_advanced,
                          'b': settings.attr_basic}.get(a))

def veure_atributs(a):
    print('\n\tAtributs: {f1}'.format(
        f1 = settings.search_fields.attributes))

def enrera(m):
    m.quit()

def quit(adObj):
    try:
        print("\nDesconnectant del Directori Actiu...")
        adObj.disconnect()
    except AttributeError:
        print("No estaves connectat al Directori Actiu")
    finally:    
        print("Adéu!!!!")
        sys.exit(0)

main_menu = """
===================================================================================================
          Menú:

    1. Selecciona un informe
    2. Mostra els paràmetres de la connexió
    3. Connecta al ldap
    4. Desconnecta del ldap
    5. Surt de l'aplicació
"""

reports_menu="""
===================================================================================================
         Informes:

    1. Usuaris del domini
    2. Equips del domini
    3. Grups del domini amb usuaris/equips
    4. Cerca personalitzada per Usuari/Equip/Grup
    5. Informes personalitzats
    6. Atributs de sortida
    7. Exporta el resultat
    8. Paràmetres exportació fitxers
    9. Enrera
"""

personalitza_menu="""
===================================================================================================
         Informes 2:

    1. Cerca per Usuari
    2. Cerca per Equip
    3. Cerca per Grup
    4. Cerca qualsevol objecte
    5. Enrera
"""

export_menu="""
===================================================================================================
         Modifica paràmetres exportació:

    1. Modifica ruta
    2. Modifica extensió
    3. Veure els paràmetres
    4. Enrera
"""

atributs_menu="""
===================================================================================================
         Modifica els atributs de les consultes:

    1. Veure atributs
    2. Atributs basics
    3. Atributs avançats
    4. Personalitza atributs
    5. Enrera
"""

personalitza_choices = {
"1": [llegeix_input,('u', ad)],
"2": [llegeix_input,('c', ad)],
"3": [llegeix_input,('g', ad)],
"4": [llegeix_input,('*', ad)],
"5": [enrera, menus['m_personalitzat']]
}

export_choices = {
"1": [modifica_param, 0],
"2": [modifica_param, 1],
"3": [veure_params, 0],
"4": [enrera, menus['m_export']]
}

atributs_choices = {
"1": [veure_atributs, 0],
"2": [mod_atributs, 'b'],
"3": [mod_atributs, 'a'],
"4": [intro_atributs, None],
"5": [enrera, menus['m_atributs']]
}

reports_choices = {
"1": [search,('u', ad)],
"2": [search,('c', ad)],
"3": [search,('g', ad)],
"4": [crear_menu, [menus['m_personalitzat'], personalitza_choices, personalitza_menu]],
"5": [crear_menu, [menus['m_informes'], settings.choices, settings.menu_txt]],
"6": [crear_menu, [menus['m_atributs'], atributs_choices, atributs_menu]],
"7": [result_export, ad],
"8": [crear_menu, [menus['m_export'], export_choices, export_menu]],
"9": [enrera, menus['m_reports']]
}

main_choices = {"3": [establir_connexio, ad],
"2": [show_connection, ad],
"1": [crear_menu, [menus['m_reports'],reports_choices,reports_menu]],
"4": [modify_connection, ad],
"5": [quit, ad]
}
