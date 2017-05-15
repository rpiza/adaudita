from connecta import ConnectaAD

obj1 = ConnectaAD()
conn=obj1.connect()


print("++++++++++USERS+++++++++++++++++++++")
obj1.get_ldap_info('(&(samAccountName=admin)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))')

print(obj1.c.response_to_json())
print(obj1.c.result)

print("++++++++++++++++++++++++++++++++++++")
print("++++++++++COMPUTERS+++++++++++++++++")
obj1.get_ldap_info('(&(samAccountName=*)(objectClass=computer)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))')

print(obj1.c.response_to_json())
print(obj1.c.result)

obj1.disconnect()
