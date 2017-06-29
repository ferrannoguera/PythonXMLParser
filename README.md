# PythonXMLParser
Python script which parses several xml
- Script que et filtra actes de la web "http://www.bcn.cat/tercerlloc/agenda_cultural.xml" i et genera un html amb una taula on et dona: Nom, Adreça, Barri, Data Inici, Data Fi i Hora del Acte en qüestió, a més de les 5 estacions de bicing a menys de 500 metres que tinguin bicis o pàrking disponibles (ordenades per proximitat) i 5 Parkings també a menys de 500 metres i ordenats per proximitat.

- Pots filtrar la consulta amb --key i un nom de barri, nom d'adreça o nom de l'acte (si s'escriuen més d'un en forma de llista s'assegura que hi siguin tots, si es en forma de tupla només s'assegura que hi hagi almenys un dels noms si és en string sol s'assegura que el nom escrit hi sigui).

- Pots filtrar també amb --date i un seguit de dates, i s'assegura que els actes que imprimeixi en la taula html estiguin en l'interval de dates seleccionat.
