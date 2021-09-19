from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
import etl

class ShopMissA(CrawlSpider):
    name = "productos"
    # USER AGENT PARA PROTEGERNOS DE BANEOS
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
    }

    allowed_domains = ['shopmissa.com']

    start_urls = [
       'https://www.shopmissa.com/collections/blenders-sponges',
       'https://www.shopmissa.com/collections/nails',
    ]

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
    
    def parse_product(self, response):
        #Extraer SKU
        sku = response.xpath('//div[@class="ProductMeta"]//span[@class="ProductMeta__SkuNumber"]/text()').get()
        # Extraer nombre del producto
        name = response.xpath('//div[@class="ProductMeta"]/h1/text()').get()
        # Extraer descripcion del producto
        text_p = response.xpath('//div[@class="ProductMeta__Description"]/div[@class="Rte"]//p/text()').getall()
        text_li = response.xpath('//div[@class="ProductMeta__Description"]/div[@class="Rte"]//li/text()').getall()
        span = response.xpath('//div[@class="ProductMeta__Description"]/div[@class="Rte"]//span/text()').getall()
        description = etl.join_description(text_p, text_li, span) 
        # Extraer categoria del producto   
        categorie =  etl.find_categorie(response)
        #Extraer url de imagenes
        images_url = response.xpath('//div[@class="AspectRatio AspectRatio--withFallback"]//img/@data-original-src').getall()
        images_url = etl.clean_images(images_url)

        if categorie != " ":
            products.append({
                "name": name,
                "description": description,
                "categorie" : categorie,
                "images": images_url,
                "sku": sku,
            })  

        
#Arreglo que tendra la informacion extraida de los productos
products = []

#Iniciar Scrapy
process = CrawlerProcess()
process.crawl(ShopMissA)
process.start()

etl.transform(products)

