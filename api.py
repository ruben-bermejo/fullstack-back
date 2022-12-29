""" API con funciones para trabajar con listas """

def obtener_primer_elemento(lista):
    """ Retorna el primer elemento de una lista """
    return lista[0]

def inserta_elemento_al_final(lista, elemento):
    """ Añade un elemento al final de la lista """
    lista.append(elemento)

def inserta_elemento_al_principio(lista, elemento):
    """ Añade un elemento al principio de la lista """
    lista.insert(0, elemento)

def borra_lista(lista):
    """ Vacía de elementos una lista """
    lista.clear()
