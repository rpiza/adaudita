import settings
from menuClass import Menu
#from collections import namedtuple
#import funcions as funcions
from connecta import ad
from exportsClass import Exports

def main():
    #Inicialitzam els parametes de l'aplicacio
    settings.init()

    #Cream l'objecte de connexio al ldap
    ad.__init__(settings.dc.host, settings.dc.port, settings.dc.usuari, settings.dc.contrasenya, settings.dc.ssl)
    e = Exports()
    #Inicialitzam els parametres de l'aplicacio que necessiten l'objecte de connexio al directori actiu
    llista_menus = settings.init_menus(ad)

    #Establim la connexio al ldap
    print("\n")
    ad.establir_connexio()

    #Mostram les dades de connexió
    ad.show_connection()

    #Cream el menu principal
    menu_principal = Menu("principal", ad, e, llista_menus)

#    try:
    menu_principal.run()
#    except:
#        pass
#    except KeyboardInterupt:
#        funcions.quit(ad)

if __name__ == "__main__":
    main()
