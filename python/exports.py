from json2html import *


def print_results(llista, json):
    ''' Imprimiex el resultat de la consulta ldap'''
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


#        print (elem) 
#    print(ad.c.result)
#    print(llista)
#    print(json)

def export_json():
    return ad.c.response_to_json()

def export_csv():
    pass

def export_pdf():
    pass

def export_xml():
    pass

def export_html():
    return '<html><head></head><h1>Titol de l informe</h1><body>' + json2html.convert(json = ad.c.response_to_json()) + '</body><html>'
