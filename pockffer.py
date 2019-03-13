from pockffer.menu import menuTitulo
from pockffer.menu import menuPrincipal
from pockffer.menu import menuSwitcher

"""
Cuerpo del pockffer que llama a las funciones de Menu.
__author__ = 'RafaLpeC'

"""

while True:
    menuTitulo()
    menuPrincipal()
    try:
        opcion = int(input("Elige una opción: "))
        menuSwitcher(opcion)
    except ValueError:
        print("Opción Invalida.")