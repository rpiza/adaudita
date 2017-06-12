from menuClass import Menu
from collections import namedtuple
import funcions as funcions
from connecta import ad

Dades_DC = namedtuple("Dades_DC", "nom host port usuari contrasenya ssl")
dc = Dades_DC("Test", 'dc1.problemeszero.com', 389, 'PZERO\\admin', 'Password1', False)

#Cream l'objecte de connexio al ldap
ad.__init__(dc.host,dc.port,dc.usuari,dc.contrasenya, dc.ssl)
#Establim la connexio al ldap
print("\n")
funcions.establir_connexio(ad)
#Mostram les dades de connexió
funcions.show_connection(ad)
#Cream el menu principal
menu_principal = Menu(funcions.main_choices,funcions.main_menu)

if __name__ == "__main__":
    try:
       menu_principal.run()
    except:
        pass
#    except KeyboardInterupt:
#        funcions.quit(ad)

