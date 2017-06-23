from collections import namedtuple

Dades_DC = namedtuple("Dades_DC", "nom host port usuari contrasenya ssl")
Dades_Search = namedtuple("Search", "nom base scope attributes")


def init():
    global dc
    global search_fields
    global filtre_consola

    dc = Dades_DC("Test", 'dc1.problemeszero.com', 389, 'PZERO\\admin', 'Password1', False)
    search_fields = Dades_Search("Dades_Search", 'DC=problemeszero,DC=com','SUBTREE', ['cn','memberOf','member'] )
    filtre_consola = None # 'cn=admin*' #Ha de ser None
