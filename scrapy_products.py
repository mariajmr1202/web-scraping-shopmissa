import requests
from PIL import Image
import io
from scrapy.http import request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class ShopMissA(CrawlSpider):
    name = "productos"
    # USER AGENT PARA PROTEGERNOS DE BANEOS
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
    }

    allowed_domains = ['shopmissa.com']

    start_urls = ['https://www.shopmissa.com/collections/skincare']

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

    def join_description(self, text_p, text_li):
        description = ""
        for text in text_p:
            text = text.replace('\xa0','')
            text = text.replace('\n','')
            description += text
        for text in text_li:
            text = text.replace('\xa0','')
            text = text.replace('\n','')
            description += text
        return description

    def find_categorie(self, url):
        categorie = str(url).replace('<200 https://www.shopmissa.com/collections/','')
        categorie = categorie[:categorie.find('/')].replace('oki-life','Life & Home').replace('spa-body','Spa & Body').replace('-',' ').title()
        return categorie
    
    def parse_product(self, response):
        # Extraer nombre del producto
        name = response.xpath('//div[@class="ProductMeta"]/h1/text()').get()
        # Extraer descripcion del producto
        text_p = response.xpath('//div[@class="ProductMeta__Description"]/div[@class="Rte"]//p/text()').getall()
        text_li = response.xpath('//div[@class="ProductMeta__Description"]/div[@class="Rte"]//li/text()').getall()
        description = self.join_description(text_p, text_li) 
        # Extraer categoria del producto   
        categorie =  self.find_categorie(response)
        #Extraer imagen
        images = response.xpath('//div[@class="AspectRatio AspectRatio--withFallback"]//img/@data-original-src').get()

        products.append({
            "name": name,
            "description": description,
            "categorie" : categorie,
            "images": images,
        })

        try:
            image_content = requests.get('https:'+images).content   
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = './images/'+ name.replace('-',' ').replace('+',' ').replace(' ','_') + '.jpg'  # nombre a guardar de la imagen
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)   
        except Exception as e:
            print(e)
            print ("Error")  

products = []

process = CrawlerProcess()
process.crawl(ShopMissA)
process.start()

print('\n\n')
print('Productos:')
print('\n\n')

# for product in products:
#     print('Name: '+ product['name'])
#     print(product['description'])
#     print('Categorie: '+product['categorie'])
#     print(product['images'])
#     print('\n')
