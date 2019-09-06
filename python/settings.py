from collections import namedtuple
import menuClass as mc

from time_functions import restar_dies_data_actual, convertir_data, convertir_data_ISO, restar_dies_data_actual_ISO
from adsClasses import uac_and_mask, uac_or_mask

Dades_DC = namedtuple('Dades_DC', 'nom host port usuari contrasenya ssl')
Search = namedtuple('Search', 'nom base scope attributes filter')


attr_basic = ['cn','memberOf','member', 'pwdlastset', 'lastlogon', 'badpasswordtime', 'whenCreated', 'userAccountControl']
attr_advanced = ['cn', 'givenname','sn', 'mail', 'admincount', 'memberOf','member', 'pwdlastset', 'lastlogon', 'badpasswordtime', 'userAccountControl', 'scriptPath']

'''Es poden crear els informes personalitzats amb el search_base, atributs i filtre que es vulgui. Aquests informes son creats
en temps d'excucio.

Camps de llista_informes:
[[Nom de l'informe, search_base, scope, atributs a retornar, filtre]]
RECORDA A INTRODUIR UNA COMA ENTRE ELS DIFERENTS INFORMES,SI NO PYTHON GENERA AQUEST ERROR:(TypeError: list indices must be integers or slices, not tuple)
'''
llista_informes = [["Informe Usuari = \'admin\'", 'DC=problemeszero,DC=com', 'SUBTREE', ['lastlogon', 'userAccountControl', 'samaccountname', 'whenchanged', 'whenCreated'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(CN=admin))', False],
                    ["Informe Equip = \'DC1\'", 'DC=problemeszero,DC=com', 'SUBTREE', attr_basic,
                        '(&(objectClass=*)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(CN=DC1))', False],
                    [ "Llistat d'usuaris que no han canviat la contrasenya fa més de 60 dies", 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['samaccountname', 'pwdlastset', 'whenCreated', 'memberof', 'userAccountControl', 'description'],
                        '(&(objectClass=*) jectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(pwdlastset<={f1}))'.format(f1=restar_dies_data_actual(60)), False],
                    ["Usuaris que pertanyen al grup 'Domain Admins'", 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'samaccountname', 'memberOf', 'whenCreated'],
                        '(&(objectClass=*) (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(memberOf=CN=Domain Admins,CN=Users,DC=problemeszero,DC=com))', False],
                    ["Informe OU = 'XXX'", 'OU=Innovacio,OU=PZERO,DC=problemeszero,DC=com', 'SUBTREE', ['lastlogon', 'userAccountControl', 'samaccountname', 'whenchanged', 'pwdlastset', 'whenCreated', 'memberof', 'description'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(CN=*))', False],
                    ["Informe OU = 'Apps'", 'OU=Apps,OU=Grups_Globals_Acces,DC=problemeszero,DC=com', 'SUBTREE', ['memberof', 'objectCategory', 'cn', 'whenchanged', 'whenCreated', 'member', 'description', 'info'],
                        '(objectClass=*)', False],
                    ["Informe OU = 'Apps' nomes CN", 'OU=Apps,OU=Grups_Globals_Acces,DC=problemeszero,DC=com', 'SUBTREE', ['cn'],
                        '(objectClass=*)', False],
                    [ "Usuaris que pertanyen al grup 'Expedients'", 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenName', 'sn', 'memberOf', 'member', 'whenCreated', 'lastLogon', 'lastLogonTimestamp', 'userAccountControl'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(memberOf:1.2.840.113556.1.4.1941:=CN=Expedients,OU=Apps,OU=Grups_Globals_Acces,DC=problemeszero,DC=com))', False],
                    [ "Usuaris que pertanyen al grup 'ComptaAytos' i subrgrups membres", 'OU=PZERO,DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenName', 'sn', 'samaccountname', 'memberOf', 'member', 'whenCreated', 'lastLogon', 'lastLogonTimestamp', 'userAccountControl'],
                        '(&(objectClass=*)(objectCategory=*)(memberOf:1.2.840.113556.1.4.1941:=CN=ComptaAYTOS,OU=Apps,OU=Grups_Globals_Acces,DC=problemeszero,DC=com))', False],
                    ["Usuaris que pertanyen al grup 'SIT_L' i subrgrups membres", 'OU=PZERO,DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenName', 'sn', 'samaccountname', 'memberOf', 'member', 'whenCreated', 'lastLogon', 'lastLogonTimestamp', 'userAccountControl'],
                        '(&(objectClass=*)(objectCategory=*)(memberOf:1.2.840.113556.1.4.1941:=CN=SIT_L,OU=SIT_Delegat,OU=Grups,DC=problemeszero,DC=com))', False],
                    ["Usuaris que pertanyen al grup 'Presto' i subrgrups membres", 'OU=PZERO,DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenName', 'sn', 'mail', 'memberOf', 'member', 'whenCreated', 'lastLogon', 'lastLogonTimestamp', 'userAccountControl'],
                        '(&(objectClass=*)(objectCategory=*)(memberOf:1.2.840.113556.1.4.1941:=CN=Presto,OU=Apps,OU=Grups_Globals_Acces,DC=problemeszero,DC=com))', False],
                    ['Usuaris amb darrer logon abans de 2016-06-09', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'samaccountname', 'memberOf', 'whenCreated', 'lastlogon'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(lastlogon<={f1}))'.
                        format(f1=convertir_data(2016, 6, 9, 20, 40)), False],
                    ['Usuaris no caduca contrasenya', 'DC=problemeszero,DC=com', 'SUBTREE',
                        [ 'cn', 'givenname', 'sn', 'pwdlastset', 'whenCreated', 'lastlogon', 'userAccountControl'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com){f1}{f2})'.
                        format(f1=uac_and_mask('ADS_UF_DONT_EXPIRE_PASSWD'), f2=uac_or_mask('ADS_UF_ACCOUNTDISABLE')), False],
                    ['Usuaris no caduca contrasenya i pwdlastset anterior a 12 mesos', 'DC=problemeszero,DC=com', 'SUBTREE',
                        [ 'cn', 'givenname', 'sn', 'pwdlastset', 'whenCreated', 'lastlogon', 'userAccountControl'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(pwdlastset<={f3}){f1}{f2})'.
                        format(f1=uac_and_mask('ADS_UF_DONT_EXPIRE_PASSWD'), f2=uac_or_mask('ADS_UF_ACCOUNTDISABLE'),f3=restar_dies_data_actual(365)), False],
                    ['Usuaris Deshabilitats', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'memberOf', 'whenCreated', 'lastlogon', 'lastLogonTimeStamp', 'userAccountControl'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com){f1})'.format(f1=uac_and_mask('ADS_UF_ACCOUNTDISABLE')), False],
                    ['Usuaris creats despres de 2017-01-01 i ADS_UF_PASSWD_NOTREQD', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'userAccountControl', 'memberOf', 'whenCreated', 'lastlogon', 'pwdlastset'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(whenCreated>={f1}){f2}{f3})'.
                        format(f1=convertir_data_ISO('2017', '01', '01'), f2=uac_and_mask('ADS_UF_PASSWD_NOTREQD'), f3=uac_or_mask('ADS_UF_ACCOUNTDISABLE')), False],
                    ['Usuaris creats despres de 2019-01-20 i no flag ADS_UF_PASSWD_NOTREQD ', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'userAccountControl', 'memberOf', 'whenCreated', 'lastlogon', 'pwdlastset'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(whenCreated>={f1}){f2}{f3})'.
                        format(f1=convertir_data_ISO('2019', '01', '20'), f2=uac_or_mask('ADS_UF_ACCOUNTDISABLE'), f3=uac_or_mask('ADS_UF_PASSWD_NOTREQD')), False],
                    ['Usuaris creats despres de 2019-01-20', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'userAccountControl', 'memberOf', 'whenCreated', 'lastlogon', 'pwdlastset'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(whenCreated>={f1}))'.
                        format(f1=convertir_data_ISO('2019', '01', '20')), False],
                    ['Usuaris deshabilitats des de 2019-01-20', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'userAccountControl', 'memberOf', 'whenCreated', 'lastlogon', 'pwdlastset'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(whenChanged>={f1}){f2})'.
                        format(f1=convertir_data_ISO('2019', '01', '20'), f2=uac_and_mask('ADS_UF_ACCOUNTDISABLE')), False],
                    ['Usuaris modificats fa mes de 30 dies i no deshabilitats', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'userAccountControl', 'memberOf', 'whenChanged', 'whenCreated', 'lastlogon'],
                        '(&(objectClass=*) (objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(whenChanged<={f1}) {f2})'.
                        format(f1=restar_dies_data_actual_ISO(30), f2=uac_or_mask('ADS_UF_ACCOUNTDISABLE')), False],
                    ['Usuaris amb NOTREQD no deshabilitats', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'userAccountControl', 'memberOf', 'whenCreated', 'lastLogon', 'lastLogonTimeStamp'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com){f1}{f2})'.
                        format(f1=uac_and_mask('ADS_UF_PASSWD_NOTREQD'), f2=uac_or_mask('ADS_UF_ACCOUNTDISABLE')), False],
                    ['Usuaris amb badpwdCount', 'DC=problemeszero,DC=com', 'SUBTREE',
                        ['cn', 'givenname', 'sn', 'userAccountControl', 'memberOf', 'whenCreated', 'lastLogon', 'lastLogonTimeStamp', 'description', 'badpwdCount', 'badpasswordtime'],
                        '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(badPwdCount>=1))', False],
                    ['Informe grups existents', 'DC=problemeszero,DC=com', 'SUBTREE', ['cn', 'description'],
                        '(&(objectClass=*)(objectCategory=CN=Group,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))', False],
                    ['Informe OUs existents dins PZERO', 'OU=PZERO,DC=problemeszero,DC=com', 'SUBTREE', ['name', 'description'],
                        '(&(objectClass=*)(objectCategory=CN=Organizational-Unit,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))', False],
                    ['Informe OUs existents excepte PZERO', 'DC=problemeszero,DC=com', 'SUBTREE', ['name', 'description'],
                        '(&(objectClass=*)(!(OU:dn:=PZERO))(objectCategory=CN=Organizational-Unit,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))', False]]

menus = {'m_reports': None, 'm_personalitzat': None, 'm_atributs': None, 'm_export': None, 'm_informes': None}

def init():
    global dc
    global search_fields
    global filtre_consola
    dc = Dades_DC('Test', 'srv.problemeszero.com', 389, 'PZERO\\admin', '12345678', False)
    search_fields = Search('basica', 'DC=problemeszero,DC=com', 'SUBTREE', attr_basic, None)
    filtre_consola = None

def init_menus(adObj):
    global menus
    for menu in menus.keys():
        menus[menu] = mc.Menu()

    return menus
