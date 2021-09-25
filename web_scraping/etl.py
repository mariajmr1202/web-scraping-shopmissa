import sheets_conexion
import PIL

categories = [
    'Makeup Brushes', 'Skincare', 'Blenders Sponges', 
    'Life & Home', 'Spa & Body', 'Face', 'Eyes', 'Lips', 
    'Nails', 'Tools', 'Makeup Bags'
]

#Guardar imagen con las dimensiones adecuadas
def clean_images(images_url):
    images = []
    for image in images_url:
        url_final = image[-17:]
        url_start = image[:-17]
        #Para imagenes jpeg
        if url_final[0] != '.':
            url_final = '.' + url_final
            url_start.pop()
        url = 'https:' + url_start + '_400x' + url_final
        images.append(url)
    return images 

#Verificar tamaño de imagenes
# def images_size(url):
#     image = requests.get(url).content
#     image_b = io.BytesIO(image).read()
#     size = len(image_b)
#     result = "{}".format(size / 1e3)
#     result = float(result)
#     sizes.append(result)

#Limpian las descripciones de los productos
def clean_description(texts, is_li):
    description = ""
    for text in texts:
        if is_li == True:
            text = text.capitalize().replace('\xa0',' ')
        else:
            text = text.replace('\xa0',' ').capitalize()
        if text.replace('\n','') == '':
            text = text.replace('\n','')
        else:
            text = text.replace('\n','. ')
        description += text
    return description    

#Une las descripciones de los productos
def join_description(text_p, text_li, span):
    description = clean_description(text_li, True)
    description += clean_description(text_p, False)
    description += clean_description(span, False)
    return description   

#Funcion que encuentra la categoria del producto
def find_categorie(url):
    categorie = str(url).replace('<200 https://www.shopmissa.com/collections/','')
    categorie = categorie[:categorie.find('/')].replace('oki-life','Life & Home').replace('spa-body','Spa & Body').replace('face-body','Face')
    categorie = categorie.replace('makeup-pouches-bags','Makeup Bags').replace('-',' ').title()
    if categorie in categories:
        return categorie
    return " "

#Elimina los productos duplicados 
def eliminate_duplicates(products):
    auxiliar = products
    try:
        for product in products:
            for aux in auxiliar:
                if product != aux and product['sku'] == aux['sku']:
                    product['categorie'] = product['categorie'] + ', ' + aux['categorie']
                    products.pop(auxiliar.index(aux))  
    except Exception as e:
        print(e)
    return products

# Dar formato a la info de los prodcutos para ser insertados en el csv
def join_attributes(products):
    string_products = []
    for product in products:
        name = str(product['name'])
        categorie = str(product['categorie'])
        description = str(product['description'])
        images = str(product['images'])
        string = ';simple;;' + name + ';1;0;visible;;' + description + ';;;taxable;;1;;;0;0;;;;;0;;;;' + categorie + ';;;'+ images +';;;;;;;;;0;;;;;;;;'
        string_products.append(string)
    return string_products

#Colocar formato Progressive a las imagenes con PIL
def progressive_images(products):
    for product in products:
        i = 1
        for url in product["images"]:
            product["images"][product["images"].index(url)] = product["sku"] + '_' + str(i)
            local_url = './images/'+ product["sku"] + '_' + str(i) +'.jpeg'
            img = PIL.Image.open(local_url)
            i+=1
            try: 
                img.save(local_url, "JPEG", quality=80, optimize=True, progressive=True)
            except Exception as e:
                print(e)
                print ("Error")


def transform(products):
    eliminate_duplicates(products)
    progressive_images(products)
    string_products = join_attributes(products)
    #Cargar data en una hoja de sheets
    sheets_conexion.load_data(string_products)
    print(len(products))