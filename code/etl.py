#Modulo de conexion a la API de Google Sheets
import sheets_conexion
#Libreria pillow para modificar imagenes
import PIL
import emoji
from googletrans import Translator

categories = [
    'Makeup Brushes', 'Skincare', 'Blenders Sponges', 
    'Life & Home', 'Spa & Body', 'Face', 'Eyes', 'Lips', 
    'Nails', 'Tools', 'Makeup Bags'
]

#Elimina emojis de los textos
def deEmojify(text):
    return emoji.get_emoji_regexp().sub(r'', text.decode('utf8'))

#Guardar imagen con las dimensiones adecuadas
def clean_images(images_url):
    images = []
    try:
        for image in images_url:
            url_final = image[-17:]
            url_start = image[:-17]
            #Para imagenes jpeg
            if url_final[0] != '.':
                url_final = '.' + url_final
                url_start = url_start[:len(url_start)-1]
            url = 'https:' + url_start + '_400x' + url_final
            images.append(url)
    except Exception as e:
        print(e)
        print('Error limpiar imagen')
        print('\n')
    return images 

#Traduccion de textos
def traslate_text(text):
    translator = Translator()
    tradu = translator.translate(text,dest='es')
    return tradu.text

#Limpia las descripciones de los productos
def clean_description(texts, is_li):
    description = ""
    try:
        for text in texts:
            text = text.replace('\xa0',' ').replace('\t','').replace('&nbsp',' ')
            text = text.encode('ascii', 'ignore').decode()
            if is_li:
                text = text.capitalize().strip()
                #Elimina lineas en blanco
                if text.replace('\n','') == '': 
                    text = text.replace('\n','')
                else:
                    text = text.replace('\n','. ')
                if len(text) > 1:
                    if text[len(text)-1] != '.' or text[len(text)-1] != ':':
                        text += '. '
            description += text
    except Exception as e:
        print(e)
        print('Error limpiar descripcion')
    description = description.strip()
    return description    

#Une las descripciones de los productos
def join_description(text_p, text_li, span):
    description = clean_description(text_p, False)
    description += clean_description(text_li, True)
    description += clean_description(span, False)
    if description != '':
        description = traslate_text(description)
    return description   

#Funcion que encuentra la categoria del producto
def find_categorie(url):
    categorie = str(url).replace('<200 https://www.shopmissa.com/collections/','')
    #Organiza el nombre de la categoria
    categorie = categorie[:categorie.find('/')].replace('oki-life','Life & Home').replace('spa-body','Spa & Body').replace('face-body','Face')
    categorie = categorie.replace('makeup-pouches-bags','Makeup Bags').replace('-',' ').title()
    #Verifica que la categoria exista, ya que por la estructura de la pagina Shopmissa, 
    #puede traer productos que no sean de ninguna categoria
    if categorie in categories:
        return categorie
    return " "

#Elimina los productos duplicados 
def eliminate_duplicates(products):
    auxiliar = products
    for product in products:
        try:
            for aux in auxiliar:
                if product != aux and product['sku'] == aux['sku']:
                    product['categorie'] = product['categorie'] + ', ' + aux['categorie']
                    products.pop(auxiliar.index(aux))  
        except Exception as e:
            print(e)
    return products

#Colocar formato Progressive a las imagenes con PIL
def progressive_images(products):
    for product in products:
        i = 1
        for url in product["images"]:
            #Asigna el nombre de las imagenes de los productos
            product["images"][product["images"].index(url)] = product["sku"] + '_' + str(i)
            #Busca las imagenes por su nombre
            local_url = './images/'+ product["sku"] + '_' + str(i) +'.jpeg'
            img = PIL.Image.open(local_url)
            i+=1
            try: 
                img.save(local_url, "JPEG", quality=80, optimize=True, progressive=True)
            except Exception as e:
                print(e)
                print ("Error")
        product["images"] = ", ".join(product["images"])


def transform(products):
    #Eliminar productos duplicados
    eliminate_duplicates(products)
    #Optimizar las imagenes de los productos
    progressive_images(products)
    #Cargar data en una hoja de sheets
    sheets_conexion.load_data(products)

