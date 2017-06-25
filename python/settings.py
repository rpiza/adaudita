from collections import namedtuple

Dades_DC = namedtuple("Dades_DC", "nom host port usuari contrasenya ssl")
Search = namedtuple("Search", "nom base scope attributes")

attr_basic = ['cn','memberOf','member', 'pwdlastset', 'lastlogon', 'badpasswordtime', 'whenCreated']
attr_advanced = ['cn', 'givenname','sn', 'mail', 'admincount', 'memberOf','member', 'pwdlastset', 'lastlogon', 'badpasswordtime']

def init():
    global dc
    global search_fields
    global filtre_consola

    dc = Dades_DC("Test", 'dc1.problemeszero.com', 389, 'PZERO\\admin', 'Password1', False)
    search_fields = Search("basica", 'DC=problemeszero,DC=com','SUBTREE', attr_basic )
    filtre_consola = None # 'cn=admin*' #Ha de ser None
