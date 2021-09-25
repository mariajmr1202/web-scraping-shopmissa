#Librerias de Scrapy para el web scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
#Modulo de Transformacion de datos
import etl

class ShopMissA(CrawlSpider):
    name = "products"

    custom_settings = {
        # USER AGENT para protegernos de baneos
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'ITEM_PIPELINES' : {'pipelines.CustomProductsImagesPipeline': 1},
        #Carpeta de las imagenes de productos
        'IMAGES_STORE' : 'images',
    }

    allowed_domains = ['shopmissa.com']

    #Urls de las categorias de shopmissa para extraer productos
    start_urls = [
        'https://www.shopmissa.com/collections/skincare',
        'https://www.shopmissa.com/collections/oki-life',
        'https://www.shopmissa.com/collections/spa-body',
        'https://www.shopmissa.com/collections/blenders-sponges',
        'https://www.shopmissa.com/collections/makeup-brushes',
        'https://www.shopmissa.com/collections/eyes',
        'https://www.shopmissa.com/collections/lips',
        'https://www.shopmissa.com/collections/face-body',
        'https://www.shopmissa.com/collections/nails',
        'https://www.shopmissa.com/collections/tools',
        'https://www.shopmissa.com/collections/makeup-pouches-bags'
    ]

    rules = (
        #Reglas para link de paginacion
        Rule(
            LinkExtractor(
                allow = r'page='
            ), follow = True
        ),
        #Reglas para link de detalle productos
        Rule(
            LinkExtractor(
                allow = r'/products/'
            ), follow = True, callback = 'parse_product'
        ),
    )
    
    def parse_product(self, response):
        #Extraer SKU del producto
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

        #Verifica que pertence a una categoria, ya que por la estructura de la pagina Shopmissa, 
        #puede traer productos que no sean de ninguna categoria
        if categorie != " ":
            products.append({
                "name": name,
                "description": description,
                "categorie" : categorie,
                "images": images_url,
                "sku": sku,
            })  

            i = 0
            #Descarga de imagenes de productos a traves de Pipeline
            for url in images_url:
                url_list = [url]
                i+=1
                name_image = sku +'_'+ str(i)
                yield {
                    'image_urls': url_list,
                    'images': name_image
                }

#Arreglo que tendra la informacion extraida de los productos
products = []

#Iniciar Scrapy
process = CrawlerProcess()
process.crawl(ShopMissA)
process.start()

#Modulo de transformacion de datos
etl.transform(products)


