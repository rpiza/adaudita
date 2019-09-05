#import funcions as funcions
#from funcions import print_results
#from connecta import ad
from funcionsClass import FuncionsMenus

class Menu():

    def __init__(self, nivell= None, adObj = None, exp = None, menus = None):
        # a default value but can also be fed in.
        if nivell:
            self.adObj = adObj
            self.exp = exp
            fm = FuncionsMenus(nivell, adObj, exp, [], menus)
            self.choices = fm.choices
            self.txt_menu = fm.txt_menu
            self.seguir = True

    def display(self):
        print(self.txt_menu)

    def run(self):
        '''Display the menu and respond to choices.'''

        while self.seguir:
            self.display()
            choice = input("Introdueix una opció: ")
#            print ('OPCIO: ',self.choices.get(choice))
            if self.choices.get(choice):
                # print (self.choices.get(choice)[1])
                action = self.choices.get(choice)[0]
                action(self.choices.get(choice)[1])
            else:
                print("{0} no és una opció vàlida".format(choice))

    def quit(self):
        self.seguir=False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
