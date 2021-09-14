import requests
from PIL import Image
import io
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

    #Funcion que encuentra la categoria del producto
    def find_categorie(self, url):
        categorie = str(url).replace('<200 https://www.shopmissa.com/collections/','')
        categorie = categorie[:categorie.find('/')].replace('oki-life','Life & Home').replace('spa-body','Spa & Body').replace('-',' ').title()
        return categorie

    #Funcion que extrae y descarga las imagenes de lo productos
    def scrapy_images(self, urls, product):
        try:
            i = 1
            for url in urls:
                image_content = requests.get('https:'+url).content   
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')
                file_path = './images/'+ product.replace('-','').replace('+',' ').replace(' ','_') +'_'+str(i)+'.jpg'  # nombre a guardar de la imagen
                with open(file_path, 'wb') as f:
                    image.save(f, "JPEG", quality=85)   
                i+=1
        except Exception as e:
            print(e)
            print ("Error") 
    
    def parse_product(self, response):
        # Extraer nombre del producto
        name = response.xpath('//div[@class="ProductMeta"]/h1/text()').get()
        # Extraer descripcion del producto
        text_p = response.xpath('//div[@class="ProductMeta__Description"]/div[@class="Rte"]//p/text()').getall()
        text_li = response.xpath('//div[@class="ProductMeta__Description"]/div[@class="Rte"]//li/text()').getall()
        description = self.join_description(text_p, text_li) 
        # Extraer categoria del producto   
        categorie =  self.find_categorie(response)
        #Extraer url de imagenes
        images_url = response.xpath('//div[@class="AspectRatio AspectRatio--withFallback"]//img/@data-original-src').getall()

        products.append({
            "name": name,
            "description": description,
            "categorie" : categorie,
            "images": images_url,
        })

        # self.scrapy_images(images_url, name)
        

products = []

process = CrawlerProcess()
process.crawl(ShopMissA)
process.start()

# print('\n\n')
# print('Productos:')
# print('\n\n')

# i = 1
# for product in products:
#     print(i)
#     print('Name: '+ product['name'])
#     print(product['description'])
#     print('Categorie: '+product['categorie'])
#     print(product['images'])
#     i+=1
#     print('\n')
