
class FuncionsMenus(adObj):


    def __init__(self, adObj, exp , export_file):
        self.adObj = adObj
        self.exp = exp
        self.export_file = export_file

    def crear_menu(m):
        '''Funcio que inicialitza un objtecte Menu()'''
        m[0].__init__(m[1],m[2])
        m[0].run()

    def search(f):
        ''' executa la funcio de search_ad i crida la funcio per imprimir els resultats'''

        c = None
        while c not in ['p','P', 'W', 'w','' ]:        
            c = input("Vols veure els resultats al navegador web o per pantalla: [W/p] ")
        if c in ['p','P']:   
            self.exp.print_results(self.adObj.search_ad_v2("llista"))
        else:
            self.exp.result_open_html(self.adObj.search_ad_v2("json")) 


def llegeix_input(f):

    print ('''Exemples de filtres de cerca:
            cn=admin*
            &(GivenName=John)(SN=Doe)
            |(GivenName=John)(GivenName=Joe)''')
    settings.filtre_consola = input("Introdueix el filtre ldap de la cerca: ")
    search(f)

def modifica_param(f):
    c = None

    self.export_files[f] = input("Introdueix el nou valor: ")

    if not os.path.exists(self.export_files[f]) and (f == 0):
        while c not in ['s','S', 'n', 'N','' ]:        
            c = input("El directori introduit no existeix. El vols crear[s/N]: ")
        if c in ['s','S']: os.makedirs(self.export_files[f])

    if (self.export_files[f] not in self.export_files[2]) and (f == 1): 
        print('Els tipus d\'extensió possibles són:', self.export_files[2])
        while c not in self.export_files[2]:        
            c = input('Tria un tipus de fitxer dels possibles. L\'extensió NO ha de incloure les \': ')
        export_files[f] = c

    def veure_params(a):
        print('\n\tDades d\'exportació actuals:\n\t\t- Ruta: {f1}\n\t\t- Extensió: {f2}\n'.format(
            f1 = self.export_files[0], f2 = self.export_files[1]))

    def result_export(adObj):
        '''Genera un fitxer amb els resultats de la darrera consulta'''
        
        #Generam un nom de fitxer aleatori
        nom_f = random_generator()
        nom_f_1 = input("\n\tNom del fitxer [{nom}]: ".format(nom = nom_f))
        if nom_f_1: nom_f = nom_f_1

        if self.exp.export_fitxer(nom_f,): 
            print(self.exp.export_fitxer(nom_f,))
            return

        while c not in ['s','S', 'n', 'N','' ]:        
            c = input('\n\tVols obrir el fitxer [s/N]: ')
        if c in ['s','S']: webbrowser.open(self.export_files[0] + '/' + nom_f + '.' + self.export_files[1])


    def intro_atributs(a):
        settings.search_fields = settings.search_fields._replace( attributes = ast.literal_eval( "[" + input(
                              'Introdueix el atributs entre \' i separats per ,\nExemple: \'cn\',\'memberOf\' :') + "]"))

    def mod_atributs(a):
        settings.search_fields = settings.search_fields._replace(attributes={'a': settings.attr_advanced,
                              'b': settings.attr_basic}.get(a))

    def veure_atributs(a):
        print('\n\tAtributs: {f1}'.format(
            f1 = settings.search_fields.attributes))

    def enrera(m):
        m.quit()

    def quit(adObj):
        try:
            print("\nDesconnectant del Directori Actiu...")
            adObj.disconnect()
        except AttributeError:
            print("No estaves connectat al Directori Actiu")
        finally:    
            print("Adéu!!!!")
            sys.exit(0)
