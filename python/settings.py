from collections import namedtuple
import menuClass as mc
# from funcions2 import search_v2, enrera_v2
from time_functions import restar_dies_data_actual, convertir_data
from adsClasses import uac_and_mask, uac_or_mask

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
llista_informes = [["Informe Usuari = \'admin\'", 'DC=problemeszero,DC=com','SUBTREE', ['lastlogon','samaccountname', 'whenchanged','whenCreated'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(CN=admin))', False],
                   ["Informe Equip = \'DC1\'", 'DC=problemeszero,DC=com','SUBTREE', attr_basic,
                        '(&(objectClass=*)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(CN=DC1))', False],
                   ["Llistat d'usuaris que no han canviat la contrasenya fa més de 60 dies", 'DC=problemeszero,DC=com','SUBTREE', \
                        ['samaccountname', 'pwdlastset','whenCreated'],'(&(objectClass=*) \
                        (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(pwdlastset<={f1}))'.format(
                        f1=restar_dies_data_actual(60)), False ],
                   ["Usuaris que pertanyen al grup \'Domain Admins\'", 'DC=problemeszero,DC=com','SUBTREE', \
                        ['cn', 'givenname', 'sn','samaccountname', 'memberOf','whenCreated'],'(&(objectClass=*) \
                        (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(memberOf=CN=Domain Admins,CN=Users,DC=problemeszero,DC=com))', False],
                   ["Usuaris amb darrer logon abans de 2016-06-09", 'DC=problemeszero,DC=com','SUBTREE', \
                        ['cn', 'givenname', 'sn','samaccountname', 'memberOf','whenCreated','lastlogon'],'(&(objectClass=*) \
                        (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(lastlogon<={f1}))'.format(
                        f1=convertir_data(2016,6,9,20,40)), False],
                   ["Usuaris no caduca contrasenya", 'DC=problemeszero,DC=com','SUBTREE', \
                        ['cn', 'givenname', 'sn','samaccountname', 'memberOf','whenCreated','lastlogon'],'(&(objectClass=*) \
                        (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com){f1}{f2})'.format(
                        f1=uac_and_mask('ADS_UF_DONT_EXPIRE_PASSWD'), f2 = uac_or_mask('ADS_UF_ACCOUNTDISABLE')), False]
                   ]

# choices = {}
# menu_txt = """
# ===================================================================================================
#          Llista d'informes personalitzats:
#
# """

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

    for menu in menus.keys():
        menus[menu] = mc.Menu()
    ##Then you can reference them with:
    #menus['m_personalitzat'].temperature()
    return menus
