#python3.5
from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS, \
    SUBTREE, \
    ALL_ATTRIBUTES
 
def get_ldap_info(filtre):
    with Connection(Server('dc1.problemeszero.com', port=389, use_ssl=False),
                    auto_bind=AUTO_BIND_NO_TLS,
                    read_only=True,
                    check_names=True,
                    user='PZERO\\admin', password='Password1') as c:
 
        c.search(search_base='DC=problemeszero,DC=com',
                 search_filter= filtre,
                 search_scope=SUBTREE,
                 #attributes=ALL_ATTRIBUTES,  #retorna tots els attr de cada objecte
                 attributes=['cn','memberOf'], #nomes retorna aquests attr.
                 get_operational_attributes=True
                 )

    print(c.response_to_json())
    print(c.result)

print("++++++++++USERS+++++++++++++++++++++")
get_ldap_info('(&(samAccountName=admin)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))')
print("++++++++++++++++++++++++++++++++++++")
print("++++++++++COMPUTERS+++++++++++++++++")
get_ldap_info('(&(samAccountName=*)(objectClass=computer)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))')


