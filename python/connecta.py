from formatters import custom_formatter
import settings
from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS, \
    SUBTREE, \
    ALL_ATTRIBUTES
import ldap3.core.exceptions


class ConnectaAD():
    'Represents '

    c = None
    resposta = []

    def __init__(self, host='localhost', port=389, u='administrator', pwd='Adm1n1strat0r', ssl = 'False', fc = None, formatter=custom_formatter):
        #this is the constructor that takes in host and port. retryAttempts is given
        # a default value but can also be fed in.
        self.host = host
        self.port = port
        self.u = u
        self.pwd = pwd
        self.ssl = ssl
        self.filtre_consola = fc
        self.custom_formatter = formatter

    def connect(self):
        '''Connecta amb el directori actiu definit.'''

        self.c = Connection(Server(self.host, port=self.port, use_ssl=self.ssl, formatter=self.custom_formatter),
            auto_bind=AUTO_BIND_NO_TLS,
            read_only=True,
            check_names=True,
            user=self.u, password=self.pwd)
        #print (self.c)

    def get_ldap_info(self,filtre):
        self.c.search(
            search_base=filtre[0],
            search_filter= filtre[1],
            search_scope=filtre[2],
            #attributes=ALL_ATTRIBUTES,  #retorna tots els attr de cada objecte
            attributes=filtre[3], #nomes retorna aquests attr.
            get_operational_attributes=filtre[4])

    def disconnect(self):
        self.c.unbind()


    def establir_connexio(self):
        ''' Estableix la connexio al DC'''
        try:
            self.connect()
            print("Connexió establerta")
        except ldap3.core.exceptions.LDAPSocketOpenError:
            print("\nEl DC no està disponible o l'adreça/port són incorrectes")
        except ldap3.core.exceptions.LDAPBindError:
            print("\nError en l'usuari o la contrasenya!!!")

    def show_connection(self):
        '''Mostra les dades de la connexio actual'''
        print("{0}: {1}\n{2}".format("Connexió", self.c,"OK"))

    def modify_connection(self):
        self.disconnect()

    def actualitza_s_filter(self,t):
        ''' Crear el filtre LDAP segons el tipus d'objecte '''
        return '(&(objectClass=*)(objectCategory={f1})({f2}))'.format(
                f1 = {'u':'CN=Person,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                      'c':'CN=Computer,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                      'g':'CN=Group,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                      '*':'*'}.get(t),
                f2 = settings.filtre_consola if settings.filtre_consola else 'CN=*')

    def actualitza_s_filter_v2(self,t):
        ''' Crear el filtre LDAP segons el tipus d'objecte '''
        return '(&(objectClass=*)(objectCategory={f1})({f2}))'.format(
                f1 = {'u':'CN=Person,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                      'c':'CN=Computer,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                      'g':'CN=Group,CN=Schema,CN=Configuration,{s_base}'.format(s_base=settings.search_fields.base),
                      '*':'*'}.get(t),
                f2 = self.filtre_consola if self.filtre_consola else 'CN=*')

    def search_ad_old(self,f):
        '''Composicio del filtre de cerca ldap, executa la cerca i
        i retorna l'objecte per a imprimir els resultats'''

        data = (settings.search_fields.base, actualitza_s_filter(f[0]), settings.search_fields.scope, settings.search_fields.attributes, False)
        print ("\n\nFiltre de cerca: ", data, "\n\nAtributs retornats: ", settings.search_fields.attributes, "\n")

        settings.filtre_consola = None
    #   Execucio de la cerca al ldap
        try:
            f[1].get_ldap_info(data)
            return f[1]
        except ldap3.core.exceptions.LDAPInvalidFilterError:
            print("\nEi!!!! Hi ha un error en el filtre!!!")
            return
        except AttributeError:
            print("\nEi!!!! Comprova que has establert la connexió al DC!!!")
            return

    def search_ad(self,f):
        '''Cerca dels Informes Personalitzats. Composicio del filtre de cerca ldap, executa la cerca i
        i retorna l'objecte per a imprimir els resultats'''

        data = (f[0][1], f[0][4], f[0][2], f[0][3], f[0][5])
        print ("\n\nFiltre de cerca: ", data, "\n\nAtributs retornats: ", f[0][3], "\n")

        self.filtre_consola = None
    #   Execucio de la cerca al ldap
        try:
            self.get_ldap_info(data)
            self.resposta = [self.c.response, self.c.response_to_json()]
            return self.c.response if f[1] == "llista" else self.c.response_to_json()
        except ldap3.core.exceptions.LDAPInvalidFilterError:
            print("\nEi!!!! Hi ha un error en el filtre!!!")
            return -1
        except ldap3.core.exceptions.LDAPSocketSendError:
            print("\nEi!!!!T'has desconnectat del DC!!!\nTorna a establir la connexió")
            return -1
        except ldap3.core.exceptions.LDAPSocketOpenError:
            print("\nEi!!!!T'has desconnectat del DC!!!\nTorna a establir la connexió")
            return -1
        except AttributeError:
            print("\nEi!!!! Comprova que has establert la connexió al DC!!!")
            return -1


ad = ConnectaAD()
