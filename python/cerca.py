from connecta import *
from ldap3 import *
from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS, \
    SUBTREE, \
    ALL_ATTRIBUTES
 

def get_ldap_info(filtre,c):
    c.search(search_base='DC=problemeszero,DC=com',
             search_filter= filtre,
             search_scope=SUBTREE,
             #attributes=ALL_ATTRIBUTES,  #retorna tots els attr de cada objecte
             attributes=['cn','memberOf'], #nomes retorna aquests attr.
             get_operational_attributes=True
             )

    print(c.response_to_json())
    print(c.result)


obj1 = ConnectaAD()
conn=obj1.connect()

print ("+++++",conn)

print("++++++++++USERS+++++++++++++++++++++")
obj1.get_ldap_info('(&(samAccountName=admin)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))')

print(obj1.c.response_to_json())
print(obj1.c.result)

print("++++++++++++++++++++++++++++++++++++")
print("++++++++++COMPUTERS+++++++++++++++++")
#get_ldap_info('(&(samAccountName=*)(objectClass=computer)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))', conn)
