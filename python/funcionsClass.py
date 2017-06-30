# import menuClass as mc
import settings

import webbrowser
import sys
import readline
import string
import random
import os
import ast

class FuncionsMenus():

    def __init__(self, nivell, adObj, exp , export_file, menus):
        self.adObj = adObj
        self.exp = exp
        self.export_file = export_file
        self.menus = menus
        # self.menus = {'m_reports': None, 'm_personalitzat': None, 'm_atributs': None, 'm_export': None, 'm_informes': None}
        # for menu in self.menus.keys():
        #     self.menus[menu] = mc.Menu()
        self.vars_menu = {'principal': self.menu_principal,
                          'informes': self.menu_informes,
                          'custom': self.menu_custom,
                          'atributs': self.menu_atributs,
                          'personalitza': self.menu_personalitza,
                          'export': self.menu_export}
        self.init_menu_var()
        self.vars_menu[nivell]()

    def menu_principal(self):
        self.txt_menu = self.main_menu
        self.choices = self.main_choices

    def menu_informes(self):
        self.txt_menu = self.reports_menu
        self.choices = self.reports_choices

    def menu_export(self):
        self.txt_menu = self.export_menu
        self.choices = self.export_choices

    def menu_atributs(self):
        self.txt_menu = self.atributs_menu
        self.choices = self.atributs_choices

    def menu_personalitza(self):
        self.txt_menu = self.personalitza_menu
        self.choices = self.personalitza_choices

    def menu_custom(self):
        choices = {}
        menu_txt = """
        ===================================================================================================
                 Llista d'informes personalitzats:

        """
        i = 1
        for elem in settings.llista_informes:
            choices.update({ str(i) : [self.search, elem]})
            menu_txt = menu_txt + "    " + str(i) + ". " + elem[0] + "\n        "
            i =  i + 1
        choices.update({ str(i) : [self.enrera, self.menus['m_informes']]})
        menu_txt = menu_txt + "    " + str(i) + ". Enrera\n"

        self.txt_menu = menu_txt
        self.choices = choices


    def crear_menu(self,m):
        '''Funcio que inicialitza un objtecte Menu()'''
        # m[0] = mc.Menu(m[1], self.adObj, self.exp)
        m[0].__init__(m[1], self.adObj, self.exp, self.menus)
        m[0].run()

    def establir_connexio(self,a):
        self.adObj.establir_connexio()

    def show_connection(self,a):
        self.adObj.show_connection()

    def modify_connection(self,a):
        self.adObj.modify_connection()

    def search(self,f):
        ''' executa la funcio de search_ad i crida la funcio per imprimir els resultats'''
        if isinstance(f,list): fltr = f
        else:
            fltr = ['nomInforme', settings.search_fields.base,
                    settings.search_fields.scope,
                    settings.search_fields.attributes,
                    self.adObj.actualitza_s_filter(f),
                    False]
        c = None
        while c not in ['p','P', 'W', 'w','' ]:
            c = input("Vols veure els resultats al navegador web o per pantalla: [W/p] ")
        if c in ['p','P']:
            self.exp.print_results(self.adObj.search_ad([fltr,"llista"]))
        else:
            self.exp.result_open_html(self.adObj.search_ad([fltr,"json"]))


    def llegeix_input(self,f):

        print ('''Exemples de filtres de cerca:
                cn=admin*
                &(GivenName=John)(SN=Doe)
                |(GivenName=John)(GivenName=Joe)''')
        settings.filtre_consola = input("Introdueix el filtre ldap de la cerca: ")
        self.search(f)

    def modifica_param(self,f):
        c = None

        self.exp.export_files[f] = input("Introdueix el nou valor: ")

        if not os.path.exists(self.exp.export_files[f]) and (f == 0):
            while c not in ['s','S', 'n', 'N','' ]:
                c = input("El directori introduit no existeix. El vols crear[s/N]: ")
            if c in ['s','S']: os.makedirs(self.exp.export_files[f])

        if (self.exp.export_files[f] not in self.exp.export_files[2]) and (f == 1):
            print('Els tipus d\'extensió possibles són:', self.exp.export_files[2])
            while c not in self.exp.export_files[2]:
                c = input('Tria un tipus de fitxer dels possibles. L\'extensió NO ha de incloure les \': ')
            self.exp.export_files[f] = c

    def veure_params(self,a):
        print('\n\tDades d\'exportació actuals:\n\t\t- Ruta: {f1}\n\t\t- Extensió: {f2}\n'.format(
            f1 = self.exp.export_files[0], f2 = self.exp.export_files[1]))

    def result_export(self,a):
        '''Genera un fitxer amb els resultats de la darrera consulta'''

        #Generam un nom de fitxer aleatori
        nom_f = self.random_generator()
        nom_f_1 = input("\n\tNom del fitxer [{nom}]: ".format(nom = nom_f))
        if nom_f_1: nom_f = nom_f_1

        if self.exp.export_fitxer(nom_f, self.adObj.resposta):
            print(self.exp.export_fitxer(nom_f, self.adObj.resposta))
            return

        c = None
        while c not in ['s','S', 'n', 'N','' ]:
            c = input('\n\tVols obrir el fitxer [s/N]: ')
        if c in ['s','S']: webbrowser.open(self.exp.export_files[0] + '/' + nom_f + '.' + self.exp.export_files[1])

    def intro_atributs(self,a):
        try:
            settings.search_fields = settings.search_fields._replace(
                                    attributes = ast.literal_eval( "[" + input(
                              'Introdueix el atributs entre \' i separats per ,\nExemple: \'cn\',\'memberOf\' :') + "]"))

        except SyntaxError:
            print('Error en la introducció dels atributs. Torna-ho a provar')

    def mod_atributs(self, a):
        settings.search_fields = settings.search_fields._replace(attributes={'a': settings.attr_advanced,
                              'b': settings.attr_basic}.get(a))

    def veure_atributs(self, a):
        print('\n\tAtributs: {f1}'.format(
            f1 = settings.search_fields.attributes))

    def enrera(self,m):
        m.quit()

    def quit(self,a):
        try:
            print("\nDesconnectant del Directori Actiu...")
            self.adObj.disconnect()
        except AttributeError:
            print("No estaves connectat al Directori Actiu")
        finally:
            print("Adéu!!!!")
            sys.exit(0)

    def random_generator(self, size = 8, chars = string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))


    def init_menu_var(self):
        self.main_menu = """
        ===================================================================================================
                  Menú:

            1. Selecciona un informe
            2. Mostra els paràmetres de la connexió
            3. Connecta al ldap
            4. Desconnecta del ldap
            5. Surt de l'aplicació
        """

        self.reports_menu="""
        ===================================================================================================
                Informes:

           1. Informes personalitzats
           2. Usuaris del domini
           3. Equips del domini
           4. Grups del domini per usuaris/equips
           5. Cerca personalitzada per Usuari/Equip/Grup
           6. Atributs de sortida
           7. Exporta el resultat
           8. Paràmetres exportació fitxers
           9. Enrera
        """

        self.personalitza_menu="""
        ===================================================================================================
                Informes 2:

           1. Cerca per Usuari
           2. Cerca per Equip
           3. Cerca per Grup
           4. Cerca qualsevol objecte
           5. Enrera
        """

        self.export_menu="""
        ===================================================================================================
                Modifica paràmetres exportació:

           1. Modifica ruta
           2. Modifica extensió
           3. Veure els paràmetres
           4. Enrera
        """

        self.atributs_menu="""
        ===================================================================================================
                Modifica els atributs de les consultes:

           1. Veure atributs
           2. Atributs basics
           3. Atributs avançats
           4. Personalitza atributs
           5. Enrera
        """

        self.personalitza_choices = {
        "1": [self.llegeix_input,'u'],
        "2": [self.llegeix_input,'c'],
        "3": [self.llegeix_input,'g'],
        "4": [self.llegeix_input,'*'],
        "5": [self.enrera, self.menus['m_personalitzat']]
        }

        self.export_choices = {
        "1": [self.modifica_param, 0],
        "2": [self.modifica_param, 1],
        "3": [self.veure_params, 0],
        "4": [self.enrera, self.menus['m_export']]
        }

        self.atributs_choices = {
        "1": [self.veure_atributs, 0],
        "2": [self.mod_atributs, 'b'],
        "3": [self.mod_atributs, 'a'],
        "4": [self.intro_atributs, None],
        "5": [self.enrera, self.menus['m_atributs']]
        }

        self.reports_choices = {
        "2": [self.search,'u'],
        "3": [self.search,'c'],
        "4": [self.search,'g'],
        "5": [self.crear_menu, [self.menus['m_personalitzat'], "personalitza"]],
        "1": [self.crear_menu, [self.menus['m_informes'], "custom"]],
        "6": [self.crear_menu, [self.menus['m_atributs'], "atributs"]],
        "7": [self.result_export, None],
        "8": [self.crear_menu, [self.menus['m_export'], "export"]],
        "9": [self.enrera, self.menus['m_reports']]
        }

        self.main_choices = {
        "3": [self.establir_connexio, None],
        "2": [self.show_connection, None],
        "1": [self.crear_menu, [self.menus['m_reports'],"informes"]],
        "4": [self.modify_connection, None],
        "5": [self.quit, None]
        }
