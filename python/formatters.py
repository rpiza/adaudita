from time_functions import convertir_temps, convertir_UTC_a_local, format_ad_timestamp_localtime, format_time_localtime
from adsClasses import trobar_flags

custom_formatter = {
'1.3.6.1.4.1.1466.115.121.1.24': (format_time_localtime, None),  # Generalized time
'1.3.6.1.4.1.1466.115.121.1.53': (format_time_localtime, None),  # Utc time  (deprecated)
'2.16.840.1.113719.1.1.5.1.19': (format_time_localtime, None),  # NDS Timestamp (Novell)
'1.2.840.113556.1.4.13': (format_ad_timestamp_localtime, None),  # builtinCreationTime (Microsoft)
'1.2.840.113556.1.4.26': (format_ad_timestamp_localtime, None),  # creationTime (Microsoft)
'1.2.840.113556.1.4.49': (format_ad_timestamp_localtime, None),  # badPasswordTime (Microsoft)
'1.2.840.113556.1.4.51': (format_ad_timestamp_localtime, None),  # lastLogoff (Microsoft)
'1.2.840.113556.1.4.52': (format_ad_timestamp_localtime, None),  # lastLogon (Microsoft)
'1.2.840.113556.1.4.96': (format_ad_timestamp_localtime, None),  # pwdLastSet (Microsoft)
'1.2.840.113556.1.4.159': (format_ad_timestamp_localtime, None),  # accountExpires (Microsoft)
'1.2.840.113556.1.4.662': (format_ad_timestamp_localtime, None),  # lockoutTime (Microsoft)
'1.2.840.113556.1.4.1696': (format_ad_timestamp_localtime, None),  # lastLogonTimestamp (Microsoft)
'1.2.840.113556.1.4.8': (trobar_flags, None)      # userAccountControl (Microsoft)
}
