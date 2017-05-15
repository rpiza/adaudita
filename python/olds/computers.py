#### Versio python 2.7

import ldap
 
l = ldap.initialize("ldap://dc1.problemeszero.com")
try:
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
 
    bind = l.simple_bind_s("admin@problemeszero.com", "Password1")
 
    base = "dc=problemeszero, dc=com"
    criteria = "(&(objectClass=computer)(cn=*))"
    attributes = ['distinguishedName', 'cn', 'lastlogon']
    result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
    results = [entry for dn, entry in result if isinstance(entry, dict)]
    print (results)
finally:
    l.unbind()
