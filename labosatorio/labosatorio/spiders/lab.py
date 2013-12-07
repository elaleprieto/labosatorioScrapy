	#from scrapy.spider import CrawlSpider
#from scrapy.contrib.spiders import CrawlSpider,Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import json
import string
import os
import time
import requests
from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from labosatorio.items import LabosatorioItem

PDF_PATH = 'pdf/'
BO_URL = "http://economia.santafe.gov.ar/compras/descargar.php?m=anexo&id={0}"
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
			print id

	# urlsCompras.append("http://economia.santafe.gov.ar/compras/site/gestion.php?idGestion=114842")

	name = 'santafe.gov.ar'
	allowed_domains = ['santafe.gov.ar']
	#start_urls = ['http://www.mininova.org/today']
	# http://economia.santafe.gov.ar/compras/site/index.php
	#start_urls = ['http://economia.santafe.gov.ar/compras/site/index.php']
#     start_urls = ['http://economia.santafe.gov.ar/compras/site/gestion.php?idGestion=114841']
	start_urls = urlsCompras

	def download(self, pliegoId, path = PDF_PATH):
		pliegos = []
		filename = '{0}.pdf'.format(pliegoId)
		filename_path = os.path.join(path, filename)
		if not os.path.exists(filename_path):
			r = requests.get(BO_URL.format(pliegoId), timeout = 1)
			with open(filename_path, 'w') as f:
				f.write(r.content)
				time.sleep(2)

		pliegos.append(filename_path)
	
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
		
		compra['monto_original'] = x.select('//div[contains(text(), "Monto Original")]/following::div[1][contains(@class, "ver-valor")]/text()').re(r'\r\n\s*(.*)\r')

		# compra['pliego'] = x.select('//div[contains(text(), "- Pliego")]/following::div[1][contains(@class, "ver-valor-lista")]/text()').re(r'\r\n\s*(.*)\r')
		compra['pliegoURL'] = x.select('//div[contains(text(), "- Pliego")]/following::div[1]//a/@href').extract()[0]
		
		index = string.find(compra['pliegoURL'], 'id=')

		compra['pliegoId'] = compra['pliegoURL'][index+3:]

		if compra['pliegoId']:
			self.download(compra['pliegoId'])
		# compra['pliegoId'] = x.select('//div[contains(text(), "- Pliego")]/following::div[1]//a').extract()
		# compra['pliegoId'] = self.driver.find_element_by_xpath('//div[contains(text(), "- Pliego")]/following::div[1]//a')
		# compra['pliegoId'] = url.get_attribute('href')
		
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
