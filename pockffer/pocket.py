"""
Funciones que vamos a emplear en pocket:
    -Control de API
    -Obtener Pockets
    -Enviar a Buffer

__author__ = 'RafaLpeC'

"""

import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen, HTTPError
from simplejson import loads
from time import sleep
from sys import exit

from pockffer.config import access_token as a_t
from pockffer.config import code_verification as c_v
from pockffer.config import consumer_key as c_k
from pockffer.config import etiqueta_pub as e_p
from pockffer.config import etiqueta_despub as e_dp
from pockffer.buffer import createArticle

"""
Función encargada de obtener el código de verificación(code_verification) utilizando la API de Pocket.

"""
def __getToken():
    url = 'https://getpocket.com/v3/oauth/request'
    post_fields = {"consumer_key":c_k,"redirect_uri":"http://www.google.com"}
    request = Request(url, urlencode(post_fields).encode())
    data = urlopen(request).read().decode()
    try:
        found = data.split('code=')[1]
        print("Código de verificación(Añadelo al archivo de configuración):",found)
        print("Visita la siguiente URL para activar tu acceso:")
        print("https://getpocket.com/auth/authorize?request_token="+found+"&redirect_uri=http://www.google.com")
        exit(0)
    except AttributeError:
        print("Lo sentimos, no hemos encontrado ningún código de verificación.")
        print("Compruebe que la 'consumer_key' sea correcta.")

"""
Función encargada de obtener el token de acceso(access_token) utilizando la API de Pocket.

"""
def __getAuthorization():
    url = 'https://getpocket.com/v3/oauth/authorize'
    data = {"consumer_key":c_k,"code":c_v}
    try:
        request = Request(url, urlencode(data).encode())
        data = urlopen(request).read().decode()
        found = data.split('&')[0]
        print("Este es tu token de acceso(access_token), añade este token al archivo de configuración:")
        print(found)
        exit(0)
    except HTTPError:
        print("Error. Comprueba que tu código de verificación es correcto.")
        print("Si no has accedido antes a la URL indicada accede a:")
        print("https://getpocket.com/auth/authorize?request_token="+c_v+"&redirect_uri=http://www.google.com")

"""
Cambia un articulo de Pocket de la etiqueta publicar a publicado
@param id ID del articulo de Pocket que va a cambiar su estado a Publicado

"""
def __setPublicado(id):
    #Eliminar la tag de publicar
    data = {"consumer_key":c_k,
            "access_token":a_t,
            "actions":[{"action":"tags_remove","item_id":id,"tags":e_p}]}
    response = requests.get("https://getpocket.com/v3/send", json=data)
    binary = response.content
    output = loads(binary)
    sleep(5)
    #Añade la tag de publicado
    data2 = {"consumer_key":c_k,
            "access_token":a_t,
            "actions":[{"action":"tags_add","item_id":id,"tags":e_dp}]}
    response2 = requests.get("https://getpocket.com/v3/send", json=data2)
    binary2 = response2.content
    output2 = loads(binary2)
    
    if(output['action_results'][0] and output2['action_results'][0]):
        print("Se han cambiado las etiqueta "+e_p + " a "+ e_dp +" correctactamente.")
    
    else:
        print('No se ha cambiado el valor de la etiqueta.')

"""
Archiva los diferentes articulos de Pockets con la etiqueta publicado.
@param id ID del articulo de Pocket que va a archivar

"""
def __setArchivar(id):
    data = {"consumer_key":c_k,
            "access_token":a_t,
            "actions":[{"action":"archive","item_id":id}]}
    response = requests.get("https://getpocket.com/v3/send", json=data)
    binary = response.content
    output = loads(binary)
    if(output['action_results'][0] == True):
        print('Se ha archivado correctactamente.')
    
    else:
        print('No se ha podido archivar.')

"""
Función que realiza la comprobación de que la API de Pocket este configurada correctamente.

"""
def API():
    if(len(c_k) == 30 and c_k[5] == "-"):
        if(len(c_v) == 30 and c_v[8] == "-" and c_v[13] == "-" and c_v[18] == "-" and c_v[23] == "-"):
            if(len(a_t) == 30 and a_t[8] == "-" and a_t[13] == "-" and a_t[18] == "-" and a_t[23] == "-"):
                print("El token es correcto")
            else:
                __getAuthorization()
        else:
            __getToken()
    else:
        print("Introduzca una 'Consumer Key' correcta en el archivo de configuración.")

"""
Lista los articulos de pocket con la etiqueta publicar(por defecto) y los devuelve
@return: Devuelve los articulos de pocket

"""
def __getPockets():
    data = dict(consumer_key=c_k,
            access_token=a_t,
            tag=e_p)
    response = requests.get("https://getpocket.com/v3/get", params=data)
    binary = response.content
    output = loads(binary)
    if output['status'] == 2:
        print("No hay pockets nuevos etiquetados para publicar.")
    return output

"""
Obtiene los articulos de Pockets, te pregunta si quieres modificar su texto,
los manda a Buffer, pasa su etiqueta a publicado(por defecto) y los archiva.

"""
def sendToBuffer():
    output = __getPockets()
    for ids in output['list']:
        print('Enviando a buffer articulo con id', ids)
        mensaje = str(output['list'][ids]['resolved_title'])
        print("Mensaje por defecto:"+mensaje+"\nURL:" + str(output['list'][ids]['given_url']))
        while True:
            pregunta = input("¿Quieres cambiar el texto del mensaje?(si o no)")
            if(pregunta == "si"):
                mensaje = str(input("Introduce el mensaje: "))
                break
            elif(pregunta == "no"):
                print("Mensaje por defecto")
                break
                
        if(createArticle(mensaje, output['list'][ids]['given_url'])):
            __setPublicado(ids)
            __setArchivar(ids)
        print('Pausa de 10 segundos...')
        sleep(10)