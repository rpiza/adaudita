import settings
from menuClass import Menu
#from collections import namedtuple
#import funcions as funcions
from connecta import ad


def main():
    #Inicialitzam els parametes de l'aplicacio
    settings.init()

    #Cream l'objecte de connexio al ldap
    ad.__init__(settings.dc.host, settings.dc.port, settings.dc.usuari, settings.dc.contrasenya, settings.dc.ssl)

    #Inicialitzam els parametres de l'aplicacio que necessiten l'objecte de connexio al directori actiu
    settings.init2(ad)
    import funcions as funcions #Abans d'importar aquest modul es necessari inicialitzar les variables del modul settings

    #Establim la connexio al ldap
    print("\n")
    funcions.establir_connexio(ad)

    #Mostram les dades de connexió
    funcions.show_connection(ad)

    #Cream el menu principal
    menu_principal = Menu(funcions.main_choices,funcions.main_menu)

#    try:
    menu_principal.run()
#    except:
#        pass
#    except KeyboardInterupt:
#        funcions.quit(ad)

if __name__ == "__main__":
    main()
