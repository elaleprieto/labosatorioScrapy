# for i in range(2001,2013):
#         url = 'http://economia.santafe.gov.ar/compras/site/AppAjax.php?a=consultas.getContrataciones&start=0&limit=100&a%C3%B1o=&bienservicio=&solicitante=&estado=AP&idEspecie=&idFamilia=&comprador=&nroExpediente=&objeto=&nroGestion=&tipoGestion=&orderBy=&anio=' + str(i)
#         print url

# for i in range(2001,2013):
#     for j in ['AP', 'ET', 'CO']:
# #         url = "estado={0}&anio={1}".format(j,i)
#         url = "http://economia.santafe.gov.ar/compras/site/AppAjax.php?a=consultas.getContrataciones&start=0&limit=100&a%C3%B1o=&bienservicio=&solicitante=&estado={0}&idEspecie=&idFamilia=&comprador=&nroExpediente=&objeto=&nroGestion=&tipoGestion=&orderBy=&anio={1}".format(j,i)
#         print url
import json

with open('contratacionesId.json', 'r') as archivo:
    datos = json.load(archivo)

for i in range(len(datos)):
    for id in datos[i]['data']:
        print id

# print datos[0]['data']

# with open('concluidas2012.json', 'r') as archivo:
#     datas = json.load(archivo)

# yahora = json.dumps(datos[0]['data'])
# vamos = json.loads(yahora)

# print datos[0]['data'][0]
# print json.dumps(datos[0]['data'])

# for key, value in datos[0].iteritems():
#     print key, value, '\n'

# for key, value in datos[0]['data'].iteritems():
#     print key, value, '\n'


# print datos
# print vamos
# print datos[0]['data']


# print datos['data']
# for i in datos["data"]:
#     print i