from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS, \
    SUBTREE, \
    ALL_ATTRIBUTES
 
class ConnectaAD():
    'Represents '

    c = None
    def __init__(self, host='localhost', port=389, u='administrator', pwd='Adm1n1strat0r'):
        #this is the constructor that takes in host and port. retryAttempts is given 
        # a default value but can also be fed in.
        self.host = host
        self.port = port
        self.u=u
        self.pwd=pwd


    def connect(self):
        """Connecta amb el directori actiu definit."""

        self.c = Connection(Server(self.host, port=self.port, use_ssl=False),
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


