"""
Funciones que vamos a emplear en buffer:
    - Comprobación del Token
    - Obtener cuentas de redes sociales asociadas a tu cuenta de Buffer
    - Creación de Articulos en Buffer

__author__ = 'RafaLpeC'

"""

import requests
from simplejson import loads
from time import sleep

from pockffer.config import token as a_t

"""
Comprueba que el Token de acceso a tu cuenta de Buffer es correcto o incorrecto.

"""
def checkToken():
    data = dict(access_token=a_t)
    response = requests.get("https://api.bufferapp.com/1/profiles.json", params=data)
    binary = response.content
    output = loads(binary)
    if 'code' not in output:
        print("Tú token de acceso es correcto.")
    else:
        if(output['code'] == 401):
            print("Error. Comprueba que tú token de acceso sea correcto en el archivo de configuración.")

"""
Lista todas las cuentas de redes sociales que tienes asociadas a tu cuenta de buffer.

"""
def __getAccountIds():
    sleep(3)
    data = dict(access_token=a_t)
    response = requests.get("https://api.bufferapp.com/1/profiles.json", params=data)
    binary = response.content
    output = loads(binary)
    accounts = []
    for ids in output:
        accounts.append(ids['_id'])
    return accounts

"""
Crea los articulos en Buffer con la información que se le pase.

@param article: Texto que va a tener el articulo que se va a crear.
@param url: URL de la noticia/articulo que va a añadir a la redacción del mensaje.
"""
def createArticle(article, url):
    listaCuentas = __getAccountIds()
    for ids in listaCuentas:
        response = requests.post("https://api.bufferapp.com/1/updates/create.json", data={'access_token':a_t,
                    'profile_ids[]':ids,
                    'text':article+" "+url})
        binary = response.content
        output = loads(binary)
        print("Cuenta de Red Social asociada a Buffer con ID "+ids+":")
        print("Respuesta de Buffer: "+ str(output))
        
        if(output['success']):
            i=+1
            print("Se ha enviado correctamente a Buffer.")
        
        else:
            print("No se ha podido enviar a Buffer el articulo.")
            print("Mensaje de Buffer: " + str(output['message']))
        print("\n")
    
    if(i == len(listaCuentas)):
        return True
        
    else:
        return False