"""
Paquete con las diferentes funciones que se van a emplear en el menu
    - Pintar el titulo
    - Pintar el menu
    - Opciones

__author__ = 'RafaLpeC'

"""


from pockffer.pocket import API;
from pockffer.pocket import sendToBuffer;
from pockffer.buffer import checkToken;
from os import system, name as osname
from sys import exit


"""
Pinta el titulo

"""
def menuTitulo():
    print("- - - - - - - - - - - - - - - - - - - - - - ")
    print("   ___           _      ___  ___ _____      ")
    print("  / _ \___   ___| | __ / __\/ __\___ / _ __ ")
    print(" / /_)/ _ \ / __| |/ // _\ / _\   |_ \| '__|")
    print("/ ___/ (_) | (__|   </ /  / /    ___) | |   ")
    print("\/    \___/ \___|_|\_\/   \/    |____/|_|   ")
    print("- - - - - - - - - - - - - - - - - - - - - - ")
    print("      Pocket to Buffer By @RafaLpeC\n")

"""
Pinta el menú con las diferentes opciones

"""
def menuPrincipal():
    print("0. Pocket API")
    print("1. Buffer API")
    print("2. Sincronizar")
    print("3. Salir")

"""
Realiza la pausa para dar ENTER y limpia la pantalla.

"""
def __menuPausa():
    input("\nPresione ENTER para continuar...")
    if osname == "posix":
        system("clear")
    elif osname == "ce" or osname == "nt" or osname == "dos":
        system("cls")

"""
Diccionario que relaciona sus indices con las diferentes funciones del menú y las ejecuta.

"""
def menuSwitcher(opcion):
    switcher={
        0:pocketAPI,
        1:bufferAPI,
        2:sincronizar,
        3:salir
        }
    
    func=switcher.get(opcion,lambda :'Opción Invalida.')
    print(func())

"""
Llama a la función API() de pocket para:
    -Obtener codigo de verificación
    -Obtener token de acceso
    -Comprobar que sea correcta la información

y realiza una pausa.

"""
def pocketAPI():
    API()
    __menuPausa()

"""
Llama a la función checkToken() de buffer para comprobar que el access_token sea correcto
y realiza una pausa

"""
def bufferAPI():
    checkToken()
    __menuPausa()

"""
Llama a la función sendToBuffer para sincronizar Pocket con Buffer y realiza una pausa

"""
def sincronizar():
    sendToBuffer()
    __menuPausa()

"""
Fin del programa.

"""
def salir():
    exit(0)