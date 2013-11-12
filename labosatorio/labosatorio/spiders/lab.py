    #from scrapy.spider import CrawlSpider
#from scrapy.contrib.spiders import CrawlSpider,Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import json
from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from labosatorio.items import LabosatorioItem

class LabSpider(BaseSpider):
    urlsCompras = []
    
#     with open('concluidas2012.json', 'r') as archivo:
#         datos = json.load(archivo)
#         
#     for i in datos["data"]:
#         urlsCompras.append("http://economia.santafe.gov.ar/compras/site/gestion.php?idGestion=" + i["idGestion"])
        
    with open('contratacionesId2001-2013.json', 'r') as archivo:
        datos = json.load(archivo)
    
    for i in range(len(datos)):
        for id in datos[i]['data']:
            urlsCompras.append("http://economia.santafe.gov.ar/compras/site/gestion.php?idGestion=" + id)
#             print id


    name = 'santafe.gov.ar'
    allowed_domains = ['santafe.gov.ar']
    #start_urls = ['http://www.mininova.org/today']
    # http://economia.santafe.gov.ar/compras/site/index.php
    #start_urls = ['http://economia.santafe.gov.ar/compras/site/index.php']
#     start_urls = ['http://economia.santafe.gov.ar/compras/site/gestion.php?idGestion=114841']
    start_urls = urlsCompras
    
    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        x = HtmlXPathSelector(response)
        compra = LabosatorioItem()
        
        #compra['titulo'] = x.select("/html/body/div/div[2]/div[5]/div/div[2]/div/h1/text()").extract() # index.php
        #compra['titulo'] = x.select('/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[contains(@class, "ver-titulo")]/text()').extract() # gestion.php
        compra['titulo'] = x.select('/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[contains(@class, "ver-titulo")]/text()').re(r'\r\n\s*(.*)\r\n') # gestion.php
        
        #compra['fecha'] = x.select("/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[23]/div[2]/text()").extract()
#         compra['fechaApertura'] = x.select("/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[23]/div[2]/text()").re(r'\r\n\s*(.*) Hs. - \r\n')
        compra['fechaApertura'] = x.select('//div[contains(text(), "Fecha y hora de apertura de ofertas")]/following::div[1][contains(@class, "ver-valor")]/text()').re(r'\r\n\s*(.*) Hs. - \r\n')
        
        #compra['monto'] = x.select("/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[25]/div[2]/text()").extract()
#         compra['monto'] = x.select('/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[25]/div[contains(@class, "ver-valor")]/text()').re(r'\r\n\s*(.*)\r')
        compra['monto'] = x.select('//div[contains(text(), "Valor del pliego")]/following::div[1][contains(@class, "ver-valor")]/text()').re(r'\r\n\s*(.*)\r')
        return compra
#     [contains(text(), "Click here")]
    #rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+']), 'parse_compra')]
    #rules = [Rule(SgmlLinkExtractor(allow=['']), 'parse_compra')]

    #def parse_compra(self, response):
        #x = HtmlXPathSelector(response)

        ##torrent = TorrentItem()
        ##torrent['url'] = response.url
        ##torrent['name'] = x.select("//h1/text()").extract()
        ##torrent['description'] = x.select("//div[@id='description']").extract()
        ##torrent['size'] = x.select("//div[@id='info-left']/p[2]/text()[2]").extract()
        
        #compra = CompraItem()
        ##compra['titulo'] = x.select("/html/body/div/div[2]/div[5]/div/div[2]/div/h1/text()").extract()
        #compra['titulo'] = x.select("/html/body/div").extract()
        ##compra['fecha'] = x.select("/html/body/div/div[2]/div[5]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/table/tbody/tr/td/div/text()").extract()
        
        
        #return compra
