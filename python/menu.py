import sys
import connecta

class Menu:
    '''Display a menu and respond to choices when run.'''
    def __init__(self):
        self.adObj = connecta.ConnectaAD()

        self.choices = {
        "1": self.show_connection,
        "2": self.establir_connexio,
        "3": self.select_report,
        "4": self.modify_connection,
        "5": self.quit
        }

        self.choices2 = {
        "1": self.search(reports["all_users"]),
        "2": self.search,
        "3": self.search,
        "4": self.search,
        "5": self.enrera
        }

        self.main_menu="""
        Menu
        1. Mostra el paràmetres de la connexió
        2. Connecta
        3. Selecciona un informe
        4. Configura el paràmetres de la connexió
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
            action = b.get(choice)
            if action:
                action()
            else:
                print("{0} no és una opció vàlida".format(choice))
 
    def show_connection(self, notes=None):
        if not notes:
            notes = self.adObj.connect()
        print("{0}: {1}\n{2}".format("Connexió", self.adObj.c,"OK"))

    def establir_connexio(self):
        self.adObj.connect()
        print("Connexió establerta")

    def search(self,f):
        self.adObj.get_ldap_info(f)
#        print(self.adObj.c.response_to_json())
#        print(self.adObj.c.result)

    def select_report(self):
        self.run(self.reports_menu, self.choices2)

    def modify_connection(self):
        id = input("Enter a note id: ")
        memo = input("Enter a memo: ")
        tags = input("Enter tags: ")
        if memo:
            self.notebook.modify_memo(id, memo)
            if tags:
                self.notebook.modify_tags(id, tags)

    def enrera(self):
        self.run(self.main_menu, self.choices)

    def quit(self):
        print("Thank you for using your notebook today.")
        self.adObj.disconnect()
        sys.exit(0)
 
reports = {
"all_users": ('DC=problemeszero,DC=com','(&(samAccountName=admin)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf'],True),
"all_computers": ('DC=problemeszero,DC=com','(&(samAccountName=admin)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf'],True),
"all_groups": ('DC=problemeszero,DC=com','(&(samAccountName=admin)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf'],True)
}
 
if __name__ == "__main__":
    Menu().run(Menu().main_menu, Menu().choices)


