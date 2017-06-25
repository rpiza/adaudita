from collections import namedtuple
import menuClass as mc
from funcions2 import search_v2, enrera_v2
import time

def restar_dies_data_actual(dies):
    '''Calcular el valor en nanosegons restant a la data actual el valor de "dies".
     Retorna el valor de windows per calcular variables de temps'''
    return (int((time.time() - (dies*86400) + 11676009600)*1e7))


Dades_DC = namedtuple("Dades_DC", "nom host port usuari contrasenya ssl")
Search = namedtuple("Search", "nom base scope attributes filter")

'''Hi ha dos grups d'atributs per defecte. Es poden configurar a desig de l'usuari. Despres en temps d'execucio es pot triar quin desl dos grups retornara la cerca o tambe hi ha l'opcio, en temps d'execucio, d'elegir els atributs a retornar'''
attr_basic = ['cn','memberOf','member', 'pwdlastset', 'lastlogon', 'badpasswordtime', 'whenCreated']
attr_advanced = ['cn', 'givenname','sn', 'mail', 'admincount', 'memberOf','member', 'pwdlastset', 'lastlogon', 'badpasswordtime']

'''Es poden crear els informes personalitzats amb el search_base, atributs i filtre que es vulgui. Aquests informes son creats
en temps d'excucio.

Camps de llista_informes:
[[Nom de l'informe, search_base, scope, atributs a retornar, filtre]]
RECORDA A INTRODUIR UNA COMA ENTRE ELS DIFERENTS INFORMES,SI NO PYTHON GENERA AQUEST ERROR:(TypeError: list indices must be integers or slices, not tuple)
'''
llista_informes = [["Informe Usuari = \'admin\'", 'DC=problemeszero,DC=com','SUBTREE', ['samaccountname', 'whenCreated'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(CN=admin))'],
                   ["Informe Equip = \'DC1\'", 'DC=problemeszero,DC=com','SUBTREE', attr_basic, 
                        '(&(objectClass=*)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(CN=DC1))'],
                   ["Llistat d'usuaris que no han canviat la contrasenya fa més de 60 dies", 'DC=problemeszero,DC=com','SUBTREE', \
                        ['samaccountname', 'pwdlastset','whenCreated'],'(&(objectClass=*) \
                        (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(pwdlastset<={f1}))'.format(
                        f1=restar_dies_data_actual(60)) ],
                   ["Usuaris que pertanyen al grup \'Domain Admins\'", 'DC=problemeszero,DC=com','SUBTREE', \
                        ['cn', 'givenname', 'sn','samaccountname', 'memberOf','whenCreated'],'(&(objectClass=*) \
                        (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(memberOf=CN=Domain Admins,CN=Users,DC=problemeszero,DC=com))']
                   ]

choices = {}
menu_txt = """
===================================================================================================
         Llista d'informes personalitzats:

"""

menus = {'m_reports': None, 'm_personalitzat': None, 'm_atributs': None, 'm_export': None, 'm_informes': None}

def init():
    global dc
    global search_fields
    global filtre_consola

    dc = Dades_DC("Test", 'dc1.problemeszero.com', 389, 'PZERO\\admin', 'Password1', False)
    search_fields = Search("basica", 'DC=problemeszero,DC=com','SUBTREE', attr_basic, None )
    filtre_consola = None # 'cn=admin*' #Ha de ser None

def init2(adObj):
    global menus
    global choices
    global menu_txt

    for menu in menus.keys():
        menus[menu] = mc.Menu()
    ##Then you can reference them with:
    #menus['m_personalitzat'].temperature()

    i = 1
    for elem in llista_informes:
        choices.update({ str(i) : [search_v2, [elem, adObj]]})
        menu_txt = menu_txt + "    " + str(i) + ". " + elem[0] + "\n"
        i =  i + 1
    choices.update({ str(i) : [enrera_v2, menus['m_informes']]})
    menu_txt = menu_txt + "    " + str(i) + ". Enrera\n"    

#time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((float(m.group(0))/1e7)-11676009600))
#convertir human readable to epoch
#int(time.mktime(time.strptime('2016-06-02T10:30:00.020', '%Y-%m-%dT%H:%M:%S.%f')))

