from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Product(Item):
    name = Field()
    price = Field()
    description = Field()
    categorie = Field()

class ShopMissA(CrawlSpider):
    name = "productos"
    # USER AGENT PARA PROTEGERNOS DE BANEOS
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
        # "FEED_URI": "productos.json",
        # "FEED_FORMAT": "json",
    }

    allowed_domains = ['shopmissa.com']

    start_urls = ['https://www.shopmissa.com/collections/eyes']

    rules = (
        #Paginacion
        Rule(
            LinkExtractor(
                allow = r'page='
            ), follow = True
        ),
        #Detalle productos
        Rule(
            LinkExtractor(
                allow = r'/products/'
            ), follow = True, callback = 'parse_product'
        ),
    )

    def find_categorie(self, url):
        categorie = str(url).replace('<200 https://www.shopmissa.com/collections/','')
        categorie = categorie[:categorie.find('/')].replace('oki-','').replace('-',' ').title()
        return categorie
 
    def quitar_simbolo_dolar(self, texto):
        nuevo_texto = texto.replace('$','')
        return nuevo_texto

    def parse_product(self, response):
        sel = Selector(response)
        item = ItemLoader(Product(), sel)

        item.add_xpath('name','//div[@class="ProductMeta"]/h1/text()')
        # item.add_xpath('description','//div[@class="ProductMeta__Description"]/div[@class="Rte"]//li/text()')       
        item.add_value('categorie', response, MapCompose(self.find_categorie))
        yield item.load_item()
