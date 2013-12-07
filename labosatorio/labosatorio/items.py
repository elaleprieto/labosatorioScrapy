# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LabosatorioItem(Item):
    # define the fields for your item here like:
    # name = Field()
    #pass
    
    titulo = Field()
    fechaApertura = Field()
    monto = Field()
    monto_original = Field()
    pliegoURL = Field()
    pliegoId = Field()


