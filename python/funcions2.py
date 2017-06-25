from connecta import ad, establir_connexio, show_connection, modify_connection, search_ad, search_ad_v2
from exports import print_results, export_html, export_json, export_csv, export_pdf, result_open_html

def search_v2(f):
    ''' executa la funcio de search_ad_v2 i crida la funcio per imprimir els resultats'''

    adObj = search_ad_v2(f)

    c = None
    while c not in ['p','P', 'W', 'w','' ]:        
        c = input("Vols veure els resultats al navegador web o per pantalla: [W/p] ")
    if c in ['p','P']:   
        print_results(adObj.c.response, adObj.c.response_to_json())
    else:
        result_open_html(adObj) 

def enrera_v2(m):
    m.quit()
