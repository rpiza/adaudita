import time
import random, string
from timezone import OffsetTzInfo
from datetime import datetime, timedelta

def restar_dies_data_actual(dies):
    '''Calcular el valor en nanosegons restant a la data actual el valor de "dies".
     Retorna el valor de windows per calcular variables de temps. Retorna els segons en valor UTC'''
    return int((time.time() - (dies*86400) + 11644473600)*1e7)

def convertir_temps(m):
    '''Convertiex la valor de temps de windows amb un string en format %Y-%m-%d %H:%M:%S. El valor m esta representat en UTC.'''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((float(m)/1e7)-11644473600))

def convertir_data(yyyy,m,d,H=0,M=0,S=0):
    '''Convertiex data amb format '%Y-%m-%dT%H:%M:%S' a valor de temps windows'''
    return int((time.mktime(time.strptime('{anyo}-{mes}-{dia}T{hora}:{minuts}:{segons}'.format(
            anyo=yyyy, mes=m, dia=d, hora=H, minuts=M, segons=S), '%Y-%m-%dT%H:%M:%S')) + 11644473600)*1e7)

def convertir_UTC_a_local(m):
    # Convert UTC datetime,format yyyymmddHHMMSS.0Z, to localtime, format %Y-%m-%d %H:%M:%S
    segons = int(time.mktime(time.strptime('{anyo}-{mes}-{dia}T{hora}:{minuts}:{segons}'.format(
                anyo=int(m[0:4]), mes=int(m[4:6]), dia=int(m[6:8]),hora=int(m[8:10]), minuts=int(
               m[10:12]), segons=int(m[12:14])), '%Y-%m-%dT%H:%M:%S')))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(segons - time.timezone + 3600) if time.localtime(
                segons-time.timezone).tm_isdst else time.localtime(segons-time.timezone))

def random_generator(size = 8, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def format_ad_timestamp(raw_value):
    """
    Active Directory stores date/time values as the number of 100-nanosecond intervals
    that have elapsed since the 0 hour on January 1, 1601 till the date/time that is being stored.
    The time is always stored in Greenwich Mean Time (GMT) in the Active Directory.
    """
    if raw_value == b'9223372036854775807':  # max value to be stored in a 64 bit signed int
        return datetime.max  # returns datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)
    try:
        timestamp = int(raw_value)
        #return datetime.fromtimestamp(time.mktime(time.localtime(timestamp/10000000.0 - 11644473600)))
        return datetime.fromtimestamp(timestamp / 10000000.0 - 11644473600, tz=OffsetTzInfo(0, 'UTC'))  # forces true division in python 2
        # return datetime.fromtimestamp(timestamp / 10000000.0 - 11644473600)  # forces true division in python 2
    except (OSError, OverflowError, ValueError):  # on Windows backwards timestamps are not allowed
        unix_epoch = datetime.fromtimestamp(0, tz=OffsetTzInfo(0, 'UTC'))
        # unix_epoch = datetime.fromtimestamp(0)
        diff_seconds = timedelta(seconds=timestamp/10000000.0 - 11644473600)
        return unix_epoch + diff_seconds
    except Exception as e:
        return raw_value

def format_time(raw_value):
    """
    """

    '''
    From RFC4517:
    A value of the Generalized Time syntax is a character string
    representing a date and time. The LDAP-specific encoding of a value
    of this syntax is a restriction of the format defined in [ISO8601],
    and is described by the following ABNF:

    GeneralizedTime = century year month day hour
                       [ minute [ second / leap-second ] ]
                       [ fraction ]
                       g-time-zone

    century = 2(%x30-39) ; "00" to "99"
    year    = 2(%x30-39) ; "00" to "99"
    month   =   ( %x30 %x31-39 ) ; "01" (January) to "09"
            / ( %x31 %x30-32 ) ; "10" to "12"
    day     =   ( %x30 %x31-39 )    ; "01" to "09"
            / ( %x31-32 %x30-39 ) ; "10" to "29"
            / ( %x33 %x30-31 )    ; "30" to "31"
    hour    = ( %x30-31 %x30-39 ) / ( %x32 %x30-33 ) ; "00" to "23"
    minute  = %x30-35 %x30-39                        ; "00" to "59"
    second      = ( %x30-35 %x30-39 ) ; "00" to "59"
    leap-second = ( %x36 %x30 )       ; "60"
    fraction        = ( DOT / COMMA ) 1*(%x30-39)
    g-time-zone     = %x5A  ; "Z"
                    / g-differential
    g-differential  = ( MINUS / PLUS ) hour [ minute ]
        MINUS           = %x2D  ; minus sign ("-")
    '''
    # if len(raw_value) < 10 or not all((c in b'0123456789+-,.Z' for c in raw_value)) or (b'Z' in raw_value and not raw_value.endswith(b'Z')):  # first ten characters are mandatory and must be numeric or timezone or fraction
    if len(raw_value) < 10 or not all((c in b'0123456789+-,.Z' for c in raw_value)) or (b'Z' in raw_value and not raw_value.endswith(b'Z')):  # first ten characters are mandatory and must be numeric or timezone or fraction
        return raw_value

    # sets position for fixed values

    year = int(raw_value[0: 4])
    month = int(raw_value[4: 6])
    day = int(raw_value[6: 8])
    hour = int(raw_value[8: 10])
    minute = 0
    second = 0
    microsecond = 0

    remain = raw_value[10:]
    if remain and remain.endswith(b'Z'):  # uppercase 'Z'
        sep = b'Z'
    elif b'+' in remain:  # timezone can be specified with +hh[mm] or -hh[mm]
        sep = b'+'
    elif b'-' in remain:
        sep = b'-'
    else:  # timezone not specified
        return raw_value

    time, _, offset = remain.partition(sep)

    if time and (b'.' in time or b',' in time):
        # fraction time
        if time[0] in b',.':
            minute = 6 * int(time[1] if str is bytes else chr(time[1]))  # Python 2 / Python 3
        elif time[2] in b',.':
            minute = int(raw_value[10: 12])
            second = 6 * int(time[3] if str is bytes else chr(time[3]))  # Python 2 / Python 3
        elif time[4] in b',.':
            minute = int(raw_value[10: 12])
            second = int(raw_value[12: 14])
            microsecond = 100000 * int(time[5] if str is bytes else chr(time[5]))  # Python 2 / Python 3
    elif len(time) == 2:  # mmZ format
        minute = int(raw_value[10: 12])
    elif len(remain) == 0:  # Z format
        pass
    elif len(time) == 4:  # mmssZ
        minute = int(raw_value[10: 12])
        second = int(raw_value[12: 14])
    else:
        return raw_value

    if sep == b'Z':  # UTC
        # timezone = None
        timezone = OffsetTzInfo(0, 'UTC')
    else:  # build timezone
        try:
            if len(offset) == 2:
                timezone_hour = int(offset[:2])
                timezone_minute = 0
            elif len(offset) == 4:
                timezone_hour = int(offset[:2])
                timezone_minute = int(offset[2:4])
            else:  # malformed timezone
                raise ValueError
        except ValueError:
            return raw_value
        if timezone_hour > 23 or timezone_minute > 59:  # invalid timezone
            return raw_value

        if str is not bytes:  # Python 3
            timezone = OffsetTzInfo((timezone_hour * 60 + timezone_minute) * (1 if sep == b'+' else -1), 'UTC' + str(
            sep + offset, encoding='utf-8'))
        else:  # Python 2
            timezone = OffsetTzInfo((timezone_hour * 60 + timezone_minute) * (1 if sep == b'+' else -1), unicode('UTC' + sep + offset, encoding='utf-8'))

    try:
        return datetime(year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute=minute,
                        second=second,
                        microsecond=microsecond
                        ,tzinfo=timezone)
    except (TypeError, ValueError):
        return raw_value

def format_ad_timestamp_localtime(raw_value, localtime=True):
    # localtime=False
    '''Deu ser un error de astimezone, no permet aplicar-se a dades anteriors a
    datetime.datetime(1901, 1, 1, 0, 15, tzinfo=datetime.timezone(datetime.timedelta(0), 'WET'))
    D'aqui la segona condicio del if clause'''
    return format_ad_timestamp(raw_value).astimezone() if localtime and (format_ad_timestamp(raw_value).timestamp() > -2177451900.0)else format_ad_timestamp(raw_value)

def format_time_localtime(raw_value, localtime=True):
    # localtime=False
    '''Deu ser un error de astimezone, no permet aplicar-se a dades anteriors a
    datetime.datetime(1901, 1, 1, 0, 15, tzinfo=datetime.timezone(datetime.timedelta(0), 'WET'))
    D'aqui la segona condicio del if clause'''
    return format_time(raw_value).astimezone() if localtime and (format_time(raw_value).timestamp() > -2177451900.0) else format_time(raw_value)

# def validate_ad_timestamp(input_value):
#     """
#     Active Directory stores date/time values as the number of 100-nanosecond intervals
#     that have elapsed since the 0 hour on January 1, 1601 till the date/time that is being stored.
#     The time is always stored in Greenwich Mean Time (GMT) in the Active Directory.
#     """
#     if not isinstance(input_value, SEQUENCE_TYPES):
#         sequence = False
#         input_value = [input_value]
#     else:
#         sequence = True  # indicates if a sequence must be returned
#
#     valid_values = []
#     changed = False
#     for element in input_value:
#         if isinstance(element, STRING_TYPES):  # tries to check if it is already be a AD timestamp
#             if isinstance(format_ad_timestamp(to_raw(element)), datetime):  # valid Generalized Time string
#                 valid_values.append(element)
#             else:
#                 return False
#         elif isinstance(element, datetime):
#             changed = True
#             if element.tzinfo:  # a datetime with a timezone
#                 valid_values.append(to_raw((timegm((element).utctimetuple()) + 11644473600) * 10000000, encoding='ascii'))
#             else:  # datetime without timezone, assumed local and adjusted to UTC
#                 offset = datetime.now() - datetime.utcnow()
#                 valid_values.append(to_raw((timegm((element - offset).timetuple()) + 11644473600) * 10000000, encoding='ascii'))
#         else:
#             return False
#
#     if changed:
#         if sequence:
#             return valid_values
#         else:
#             return valid_values[0]
#     else:
#         return True
#
# def validate_time(input_value):
#     # if datetime object doesn't have a timezone it's considered local time and is adjusted to UTC
#     if not isinstance(input_value, SEQUENCE_TYPES):
#         sequence = False
#         input_value = [input_value]
#     else:
#         sequence = True  # indicates if a sequence must be returned
#
#     valid_values = []
#     changed = False
#     for element in input_value:
#         if isinstance(element, STRING_TYPES):  # tries to check if it is already be a Generalized Time
#             if isinstance(format_time(to_raw(element)), datetime):  # valid Generalized Time string
#                 valid_values.append(element)
#             else:
#                 return False
#         elif isinstance(element, datetime):
#             changed = True
#             if element.tzinfo:  # a datetime with a timezone
#                 valid_values.append(element.strftime('%Y%m%d%H%M%S%z'))
#             else:  # datetime without timezone, assumed local and adjusted to UTC
#                 offset = datetime.now() - datetime.utcnow()
#                 valid_values.append((element - offset).strftime('%Y%m%d%H%M%SZ'))
#         else:
#             return False
#
#     if changed:
#         if sequence:
#             return valid_values
#         else:
#             return valid_values[0]
#     else:
#         return True
