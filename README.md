#BRANCA EN DESENVOLUPAMENT. SELECCIONA master


# Auditoria d'Active Directory - ADaudita

Aplicació d'auditoria de Directori Actiu

Necessita la version python 3.5 o superior

Es necessari configurar el fitxer **settings.py** amb els paràmetres del teu entorn

Per obrir el programa executa la següent comanda:

 *#python python/main.py*

### Configuració personalitzada d'informes

Es poden configurar informes personalitzats afegint una llista a la variable **llista_informes** del fitxer **settings.py**. Aquests informes es mostren en temps d'execució a l'opcio:
<pre>
===================================================================================================
         Informes:

    1. Usuaris del domini
    2. Equips del domini
    3. Grups del domini per usuaris/equips
    4. Cerca personalitzada per Usuari/Equip/Grup
    <b>5. Informes personalitzats</b>
    6. Atributs de sortida
    7. Exporta el resultat
    8. Paràmetres exportació fitxers
    9. Enrera
</pre>

Per a crear un informe personaltitzat editam el fitxer **settings.py** i afegim una llista semblant a la seguent:
<pre>
["Usuaris que pertanyen al grup \'Domain Admins\'", 'DC=problemeszero,DC=com','SUBTREE',['cn', 'givenname', 'sn','samaccountname', 'memberOf','whenCreated'],'(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(memberOf=CN=Domain Admins,CN=Users,DC=problemeszero,DC=com))']
</pre>

On:
+ Nom de l'informe = "Usuaris que pertanyen al grup \'Domain Admins\'"
+ Search Base = 'DC=problemeszero,DC=com'
+ Scope = 'SUBTREE'
+ Atributs retornats = ['cn', 'givenname', 'sn','samaccountname', 'memberOf','whenCreated']
+ Filtre de cerca = '(&(objectClass=*)(objectCategory=CN=Person,CN=Schema,CN=Configuration,DC=problemeszero,DC=com)(memberOf=CN=Domain Admins,CN=Users,DC=problemeszero,DC=com))'



### Problemes detectats

El desenvolupament de l'eina s'ha realitzat amb un client Ubuntu 16.04.   
Hem detectat algun problema a l'hora d'executar l'aplicació amb clients amb sistema operatiu Windows. Sobretot en la presentació dels informes i en la conversió dels valors de temps, propis de windows, a valors de data utiltzats per l'aplicació.

Als entorns Windows el mòdul **readline** no és necessari. Es pot comentar la linia que hi fa referència del fitxer **funcions.py**, si vos genera errors.

Heu de tenir en compte que els **Informes personalitzats** inclosos en el fitxer **settings.py**, tenen els filtres dels objectes configurats amb el search_base de l'entorn de proves. Per a que vos funcionin correctament, els heu configurar adequadament amb els paràmetres del vostre entorn.
