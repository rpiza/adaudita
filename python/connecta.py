from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS, \
    SUBTREE, \
    ALL_ATTRIBUTES
 
class ConnectaAD():
    c = None
    def __init__(self, host='dc1.problemeszero.com', port=389, u='PZERO\\admin', pwd='Password1'):
        #this is the constructor that takes in host and port. retryAttempts is given 
        # a default value but can also be fed in.
        self.host = host
        self.port = port
        self.u=u
        self.pwd=pwd


    def connect(self):
        self.c = Connection(Server(self.host, port=self.port, use_ssl=False),
            auto_bind=AUTO_BIND_NO_TLS,
            read_only=True,
            check_names=True,
            user=self.u, password=self.pwd)
        #print (self.c)

    def get_ldap_info(self,filtre):
        self.c.search(
            search_base='DC=problemeszero,DC=com',
            search_filter= filtre,search_scope=SUBTREE,
            #attributes=ALL_ATTRIBUTES,  #retorna tots els attr de cada objecte
            attributes=['cn','memberOf'], #nomes retorna aquests attr.
            get_operational_attributes=True)

    def disconnect(self):
        pass


