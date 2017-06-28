''' Aquest modul inclou les funcions d'exportacio implementades'''

from json2html import *
import webbrowser
import tempfile
import sys
import ldap3.core.exceptions
import re
from taulaClass import Taula
from time_functions import convertir_temps, convertir_UTC_a_local



def print_results(llista, json):
    ''' Imprimiex el resultat de la consulta ldap per pantalla
    La variable amplada_col marca l'amplada de les columnes. Si es retornen massa atributs, els resultats
    es superposen i no es veu correctament'''

    amplada_col= 20 
    taula = Taula(results_2(llista), amplada_col, True, "|", "-")
    print(taula)

def export_json(adObj):
    return re.sub(r'\d{14}.\d{,3}Z|\d{18}', convertir_cerca, adObj.c.response_to_json(), count=0, flags=0)

def export_csv(adObj):
    return re.sub(r'\d{14}.\d{,3}Z|\d{18}', convertir_cerca, results(adObj.c.response), count=0, flags=0)
    #return results(adObj.c.response)

def export_pdf(adObj):
    return ("En proces de desenvolupament")


def export_html(adObj):
    html = '<html><head></head><h1>Titol de l informe</h1><body>' + json2html.convert(
        json = adObj.c.response_to_json()).replace('<th>entries</th>','') + '</body><html>'
#    return html
    return re.sub(r'\d{14}.\d{,3}Z|\d{18}', convertir_cerca, html, count=0, flags=0)

def result_open_html(adObj):
    '''Obri el resultats de la darrera consulta a l'aplicacio html'''  
    try:
        fp = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        fp.write(str.encode(export_html(adObj)))
        fp.seek(0)
        webbrowser.open(fp.name)   
    except:
        print ("Unexpected error:", sys.exc_info()[0]) 
        return

def results(llista):
    ''' Crear el resultat de la consulta ldap en format csv'''
    separador = "\t"

    atributs = []
    for elem in llista:
        if elem.get('attributes'): atributs = atributs + list(elem.get('attributes').keys())    
    atributs = sorted(set(atributs))
    print(atributs)
    contingut = "dn\t" + str(atributs)[2:-2].replace("', '","\t") +"\n"        
    for elem in llista:
        if elem.get('dn'):
            contingut = contingut + str(elem.get('dn')) + "\t"
        for atribut in atributs:
            if elem.get('attributes'):
                if elem.get('attributes').get(atribut):
                    contingut = contingut + str(elem.get('attributes').get(atribut)).replace("\', \'", "; ") + "\t"
                else : contingut = contingut + "\t"       
        contingut = contingut[:-1] + "\n"       
    return contingut



def results_2(llista):
    ''' Crear el resultat de com un llista de llistes. Els atributs de Cada objecte ldap corresponen a un llista'''

    atributs = []
    for elem in llista:
        if elem.get('attributes'): atributs = atributs + list(elem.get('attributes').keys())  
  
    atributs = sorted(set(atributs))
    atributs.insert(0,'dn')
#    print(atributs)

    contingut = []
    contingut.append(atributs) 
      
    for elem in llista:
        linia = []

        if elem.get('dn'):
            linia.append(str(elem.get('dn')))

        for atribut in atributs:
            if elem.get('attributes') and atribut != 'dn':
                if elem.get('attributes').get(atribut):
                    if isinstance(elem.get('attributes').get(atribut),list):
                        linia.append(re.sub(r'\d{14}.\d{,3}Z|\d{18}', convertir_cerca,str(
                                    elem.get('attributes').get(atribut)).replace("\', \'", "; ")[2:-2], count=0, flags=0))
                    else: linia.append(re.sub(r'\d{14}.\d{,3}Z|\d{18}', convertir_cerca,str(
                                    elem.get('attributes').get(atribut)), count=0, flags=0))
                else : linia.append('')       
        if linia: contingut.append(linia)       
    return contingut


def convertir_cerca(m):
    '''Depenent del resultat de la cerca amb re.sub executa la conversio ISO o la epoch'''
    return convertir_UTC_a_local(m.group(0)) if 'Z' in m.group(0) else convertir_temps(m.group(0))


