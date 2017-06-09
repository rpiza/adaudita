from menuClass import Menu
from collections import namedtuple
import funcions as funcions
from connecta import ad

Dades_DC = namedtuple("Dades_DC", "nom host port usuari contrasenya")
dc = Dades_DC("Test", 'dc1.problemeszero.com', 389, 'PZERO\\admin', 'Password1')

ad.__init__(dc.host,dc.port,dc.usuari,dc.contrasenya)
menu_principal = Menu(funcions.main_choices,funcions.main_menu)

if __name__ == "__main__":
    menu_principal.run()

