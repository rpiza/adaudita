import sys
import connecta
from collections import namedtuple
from funcions import print_results
import menuClass

Dades_DC = namedtuple("Dades_DC", "nom host port usuari contrasenya")
dc = Dades_DC("Test", 'dc1.problemeszero.com', 389, 'PZERO\\admin', 'Password1')

reports = {
"all_users": ('DC=problemeszero,DC=com','(&(samAccountName=*)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf','accountExpires','altSecurityIdentities','badPasswordTime', 'codePage','countryCode', 'homeDirectory','homeDrive','lastLogoff','lastLogon','lmPwdHistory','logonCount','mail','maxStorage',
'ntPwdHistory','otherMailbox','PasswordExpirationDate','primaryGroupID','profilePath','pwdLastSet',
'sAMAccountType','scriptPath','unicodePwd','userAccountControl','userCertificate','userSharedFolder',
'userWorkstations'],True),
"all_computers": ('DC=problemeszero,DC=com','(&(samAccountName=*)(objectClass=computer)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf'],True),
"all_groups": ('DC=problemeszero,DC=com','(&(objectClass=*)(objectCategory=CN=Group,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','member'],True)
}


class Menu:
    '''Display a menu and respond to choices when run.'''
    def __init__(self):
        self.adObj = connecta.ConnectaAD(dc.host,dc.port,dc.usuari,dc.contrasenya)

        self.choices = {
        "1": self.establir_connexio,
        "2": self.show_connection,
        "3": self.select_report,
        "4": self.modify_connection,
        "5": self.quit
        }

        self.choices2 = {
        "1": self.search_all_users,
        "2": self.search_all_computers,
        "3": self.search_all_groups,
        "4": self.search,
        "5": self.enrera
        }

        self.main_menu="""
        Menú
        1. Connecta
        2. Mostra el paràmetres de la connexió
        3. Selecciona un informe
        4. Desconnecta
        5. Surt
        """

        self.reports_menu="""
        Informes:
        1. Usuaris del domini
        2. Equips del domini
        3. Grups del domini amb usuaris/equips
        4. Extra
        5. Enrera
        """

    def display_menu(self, a):
        print(a)

    def run(self,a,b):
        '''Display the menu and respond to choices.'''

        while True:
            self.display_menu(a)
            choice = input("Introdueix una opció: ")
            ''' Si estam al menu principal no passam parametre a action. Si estam a una altre menu, passam com a parametre el report'''
            action = b.get(choice) if a[9:13] == "Menú" else b.get(choice)(reports["all_users"])             
            if action:
                action()
            else:
                print("{0} no és una opció vàlida".format(choice))
 
    def select_report(self):
        '''Mostra el menu dels diferents reports configurats.'''
        self.run(self.reports_menu, self.choices2)

    def show_connection(self):
        print("{0}: {1}\n{2}".format("Connexió", self.adObj.c,"OK"))

    def establir_connexio(self):
        self.adObj.connect()
        print("Connexió establerta")
       #print("{0}: {1}\n{2}".format("Connexió", adObj.c,"OK"))

    def search(self,f):
        self.adObj.connect()
        self.adObj.get_ldap_info(f)
        print_results(self.adObj.c.response,self.adObj.c.response_to_json())

    def search_all_users(self,f=reports["all_users"]):
        self.adObj.get_ldap_info(f)
        print_results(self.adObj.c.response,self.adObj.c.response_to_json())

    def search_all_computers(self,f=reports["all_computers"]):
        self.adObj.get_ldap_info(f)
        print_results(self.adObj.c.response,self.adObj.c.response_to_json())

    def search_all_groups(self,f=reports["all_groups"]):
        self.adObj.get_ldap_info(f)
        print_results(self.adObj.c.response,self.adObj.c.response_to_json())

    def modify_connection(self):
        self.adObj.disconnect()

    def enrera(self):
        self.run(self.main_menu, self.choices)

    def quit(self):
        print("Adéu!!!!")
        self.adObj.disconnect()
        sys.exit(0)

