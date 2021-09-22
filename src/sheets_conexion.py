import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def conexion():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("../sheets_credencials.jsonsheets_credencials.json", scope)
    client = gspread.authorize(creds) 
    sheet = client.open("missy").sheet1    
    return sheet

def load_data(products):
    sheet = conexion()
    df = pd.DataFrame(products, columns=["ID;Tipo;SKU;Nombre;Publicado;¿Está destacado?;Visibilidad en el catálogo;Descripción corta;Descripción;Día en que empieza el precio rebajado;Día en que termina el precio rebajado;Estado del impuesto;Clase de impuesto;¿En inventario?;Inventario;Cantidad de bajo inventario;¿Permitir reservas de productos agotados?;¿Vendido individualmente?;Peso (kg);Longitud (cm);Anchura (cm);Altura (cm);¿Permitir valoraciones de clientes?;Nota de compra;Precio rebajado;Precio normal;Categorías;Etiquetas;Clase de envío;Imágenes;Límite de descargas;Días de caducidad de la descarga;Superior;Productos agrupados;Ventas dirigidas;Ventas cruzadas;URL externa;Texto del botón;Posición;Nombre del atributo 1;Valor(es) del atributo 1;Atributo visible 1;Atributo global 1;ID de descarga 1;Nombre de la descarga 1;URL de la descarga 1;"])
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

