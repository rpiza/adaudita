import time


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


#time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((float(m.group(0))/1e7)-11676009600))
#convertir human readable to epoch
#int(time.mktime(time.strptime('2016-06-02T10:30:00.020', '%Y-%m-%dT%H:%M:%S.%f')))
