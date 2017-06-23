''' Aquest modul inclou les funcions d'exportacio implementades'''

from json2html import *
import webbrowser
import tempfile
import sys
import ldap3.core.exceptions

def print_results(llista, json):
    ''' Imprimiex el resultat de la consulta ldap per pantalla'''
    for elem in llista:
#        if isinstance(elem,ldap3.utils.ciDict.CaseInsensitiveDict):
        if elem.get('dn'):
            print('\n\nDistinguished Name: ', elem.get('dn'))
        if isinstance(elem.get('attributes'),ldap3.utils.ciDict.CaseInsensitiveDict):
            for k, v in elem.get('attributes').items():

                if isinstance(v,list):
                    print(k,":")
                    for e in v: print ("\t", e)
#            print ("memberOf: ", elem.get('attributes').get('memberOf'))

def export_json(adObj):
    return adObj.c.response_to_json()

def export_csv(adObj):
    return results(adObj.c.response)

def export_pdf(adObj):
    pass

def export_xml(adObj):
    pass

def export_html(adObj):
    return '<html><head></head><h1>Titol de l informe</h1><body>' + json2html.convert(
        json = adObj.c.response_to_json()).replace('<th>entries</th>','') + '</body><html>'

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
    ''' Imprimiex el resultat de la consulta ldap per pantalla'''
    atributs = []
    for elem in llista:
        if elem.get('attributes'): atributs = atributs + list(elem.get('attributes').keys())    
    atributs = sorted(set(atributs))
    print(atributs)
    contingut = "\'dn\'\t" + str(atributs)[2:-2].replace(", ","\t") +"\n"        
    for elem in llista:
        if elem.get('dn'):
            contingut = contingut + str(elem.get('dn')) + "\t"
        for atribut in atributs:
            if elem.get('attributes'):
                if elem.get('attributes').get(atribut):
                    contingut = contingut + str(elem.get('attributes').get(atribut))[2:-2].replace("\', \'", "; ") + "\t"
                else : contingut = contingut + "\t"       
        contingut = contingut[:-1] + "\n"       
    return contingut
