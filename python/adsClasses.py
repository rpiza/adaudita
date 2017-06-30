from enum import IntEnum

#@unique
class AdsUserFlagEnum(IntEnum):
    # https://support.microsoft.com/ca-es/help/305144/

    ADS_UF_SCRIPT                                  = 1        # 0x1
    ADS_UF_ACCOUNTDISABLE                          = 2        # 0x2
    ADS_UF_HOMEDIR_REQUIRED                        = 8        # 0x8
    ADS_UF_LOCKOUT                                 = 16       # 0x10
    ADS_UF_PASSWD_NOTREQD                          = 32       # 0x20
    ADS_UF_PASSWD_CANT_CHANGE                      = 64       # 0x40
    ADS_UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED         = 128      # 0x80
    ADS_UF_TEMP_DUPLICATE_ACCOUNT                  = 256      # 0x100
    ADS_UF_NORMAL_ACCOUNT                          = 512      # 0x200
    ADS_UF_INTERDOMAIN_TRUST_ACCOUNT               = 2048     # 0x800
    ADS_UF_WORKSTATION_TRUST_ACCOUNT               = 4096     # 0x1000
    ADS_UF_SERVER_TRUST_ACCOUNT                    = 8192     # 0x2000
    ADS_UF_DONT_EXPIRE_PASSWD                      = 65536    # 0x10000
    ADS_UF_MNS_LOGON_ACCOUNT                       = 131072   # 0x20000
    ADS_UF_SMARTCARD_REQUIRED                      = 262144   # 0x40000
    ADS_UF_TRUSTED_FOR_DELEGATION                  = 524288   # 0x80000
    ADS_UF_NOT_DELEGATED                           = 1048576  # 0x100000
    ADS_UF_USE_DES_KEY_ONLY                        = 2097152  # 0x200000
    ADS_UF_DONT_REQUIRE_PREAUTH                    = 4194304  # 0x400000
    ADS_UF_PASSWORD_EXPIRED                        = 8388608  # 0x800000
    ADS_UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION  = 16777216  # 0x1000000

# (&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.804:=65536))
# Nomes usuaris actius (&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))

def uac_and_mask (nom):
    return '(userAccountControl:1.2.840.113556.1.4.804:={f1})'.format(f1 = AdsUserFlagEnum[nom])

def uac_or_mask (nom):
    return '(!(userAccountControl:1.2.840.113556.1.4.803:={f1}))'.format(f1 = AdsUserFlagEnum[nom])
