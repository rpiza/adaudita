#import funcions as funcions
#from funcions import print_results
#from connecta import ad

class Menu():

    def __init__(self, choices, txt_menu): 
        # a default value but can also be fed in.
        self.choices = choices
        self.txt_menu = txt_menu
#        self.adObj = adObj
        self.seguir = True

    def display(self):
        print(self.txt_menu)

    def run(self):
        '''Display the menu and respond to choices.'''

        while self.seguir:
            self.display()
            choice = input("Introdueix una opció: ")
#            print ('OPCIO: ',self.choices.get(choice))
#            action = self.choices.get(choice)[0]
            if self.choices.get(choice):
#                print (self.choices.get(choice)[1])
                action = self.choices.get(choice)[0]
                action(self.choices.get(choice)[1])
            else:
                print("{0} no és una opció vàlida".format(choice))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
