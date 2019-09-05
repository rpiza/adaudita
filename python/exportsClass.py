''' Aquest modul inclou les funcions d'exportacio implementades'''

from json2html import *
import webbrowser
import tempfile
import sys
import ldap3.core.exceptions
import re
import os
from taulaClass import Taula
from time_functions import convertir_temps, convertir_UTC_a_local

class Exports():

    def __init__(self, llista = None, json = None, amplada_col=20, separador = '\t',
                    export_files = ['./exports', 'csv', ('csv', 'json', 'pdf', 'html')]):
        self.llista = llista
        self.json = json
        self.amplada_col = amplada_col
        self.separador = separador
        self.export_files = export_files

    def print_results(self, llista):
        ''' Imprimiex el resultat de la consulta ldap per pantalla
        La variable amplada_col marca l'amplada de les columnes. Si es retornen massa atributs, els resultats
        es superposen i no es veu correctament'''
        if llista != -1:
            taula = Taula(self.results_2(llista), self.amplada_col, True, "|", "-")
            print(taula)

    def export_json(self,json):
        return json
        #return re.sub(r'\d{14}.\d{,3}Z|\d{18}', self.convertir_cerca, json, count=0, flags=0)

    def export_csv(self,llista):
        return self.results(llista)
        # return re.sub(r'\d{14}.\d{,3}Z|\d{18}', self.convertir_cerca, self.results(llista), count=0, flags=0)
        #return results(adObj.c.response)

    def export_pdf(self):
        return ("En proces de desenvolupament")

    def export_html(self, j):
        html = '<html><head></head><h1>Titol de l informe</h1><body>' + json2html.convert(
            json = j).replace('<th>entries</th>','') + '</body></html>'
        return html
        #return re.sub(r'\d{14}.\d{,3}Z|\d{18}', self.convertir_cerca, html, count=0, flags=0)

    def result_open_html(self,json):
        '''Obri el resultats de la darrera consulta a l'aplicacio html'''
        try:
            if json != -1:
                fp = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
                fp.write(str.encode(self.export_html(json)))
                fp.seek(0)
                webbrowser.open(fp.name)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            return

    def results(self,llista):
        ''' Crear el resultat de la consulta ldap en format csv'''
        atributs = []
        for elem in llista:
            if elem.get('attributes'): atributs = atributs + list(elem.get('attributes').keys())
        atributs = sorted(set(atributs))
        print(atributs)
        contingut = "dn"+ self.separador + str(atributs)[2:-2].replace("', '", self.separador) +"\n"
        for elem in llista:
            if elem.get('dn'):
                contingut = contingut + str(elem.get('dn')) + self.separador
            for atribut in atributs:
                if elem.get('attributes'):
                    if elem.get('attributes').get(atribut):
                        contingut = contingut + str(elem.get('attributes').get(atribut)).replace("\', \'", "; ") + self.separador
                    else : contingut = contingut + self.separador
            contingut = contingut[:-1] + "\n"
        return contingut

    def results_2(self, llista):
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
                            linia.append(str(elem.get('attributes').get(atribut)).replace("\', \'", "; ")[2:-2])
                            # linia.append(re.sub(r'\d{14}.\d{,3}Z|\d{18}', self.convertir_cerca,str(
                            #             elem.get('attributes').get(atribut)).replace("\', \'", "; ")[2:-2], count=0, flags=0))
                        else: linia.append(str(elem.get('attributes').get(atribut)))
                        # else: linia.append(re.sub(r'\d{14}.\d{,3}Z|\d{18}', self.convertir_cerca,str(
                        #                 elem.get('attributes').get(atribut)), count=0, flags=0))
                    else : linia.append('')
            if linia: contingut.append(linia)
        return contingut

    def export_fitxer(self, nom_f, llista):
        '''Genera un fitxer amb els resultats de la darrera consulta'''
        c = None

        if not os.path.exists(self.export_files[0]):
            return '\nEl directori d\'exportació: \'{f1}\', no existeix!!!\nRevisa els paràmetres d\'exportació de fitxers'.format(
                f1 = self.export_files[0])

        print('\n\tEl resultat es guardarà a ', self.export_files[0] + '/' + nom_f + '.' + self.export_files[1])
    #try:
        f = open(self.export_files[0] + '/' + nom_f + '.' + self.export_files[1], 'w')
        f.write({'json': self.export_json,
                  'csv': self.export_csv,
                  'pdf': self.export_pdf,
                  'html': self.export_html}.get(
                  self.export_files[1])(llista[{'json': 1,
                                                'csv': 0,
                                                'pdf': 1,
                                                'html': 1}.get(self.export_files[1])]))
        f.close()
        return None

    def convertir_cerca(self, m):
        '''Depenent del resultat de la cerca amb re.sub executa la conversio ISO o la epoch'''
        return convertir_UTC_a_local(m.group(0)) if 'Z' in m.group(0) else convertir_temps(m.group(0))


    # def random_generator(size=8, chars=string.ascii_lowercase + string.digits):
    #     return ''.join(random.choice(chars) for x in range(size))
