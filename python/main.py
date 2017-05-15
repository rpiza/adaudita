from menu import Menu
from collections import namedtuple

Dades_DC = namedtuple("Dades_DC", "nom host port usuari contrasenya")
dc = Dades_DC("Test", 'dc1.problemeszero.com', 389, 'PZERO\\admin', 'Password1')

reports = {
"all_users": ('DC=problemeszero,DC=com','(&(samAccountName=*)(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf','accountExpires','altSecurityIdentities','badPasswordTime', 'codePage','countryCode', 'homeDirectory','homeDrive','lastLogoff','lastLogon','lmPwdHistory','logonCount','mail','maxStorage',
'ntPwdHistory','otherMailbox','PasswordExpirationDate','primaryGroupID','profilePath','pwdLastSet',
'sAMAccountType','scriptPath','unicodePwd','userAccountControl','userCertificate','userSharedFolder',
'userWorkstations'],True),
"all_computers": ('DC=problemeszero,DC=com','(&(samAccountName=*)(objectClass=computer)(objectCategory=CN=Computer,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','memberOf'],True),
"all_groups": ('DC=problemeszero,DC=com','(&(objectClass=*)(objectCategory=CN=Group,CN=Schema,CN=Configuration,DC=problemeszero,DC=com))','SUBTREE',['cn','member'],True)
}

if __name__ == "__main__":
    Menu().run(Menu().main_menu, Menu().choices)


