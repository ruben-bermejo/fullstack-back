""" Pruebas para el módulo api """
import api

def test_obtener_primer_elemento():
    """ Prueba unitaria para obtener_primer_elemento() """
    lista = ["master", "full", "stack"]
    elemento = api.obtener_primer_elemento(lista)
    assert elemento == "master"

def test_inserta_elemento_al_final():
    """ Prueba unitaria para inserta_elemento_al_final """
    lista = ["master", "full", "stack"]
    api.inserta_elemento_al_final(lista, "hola")
    assert lista[len(lista)-1] == "hola"

def test_inserta_elemento_al_principio():
    """ Prueba unitaria para inserta_elemento_al_principio """
    lista = ["master", "full", "stack"]
    api.inserta_elemento_al_principio(lista, "hola")
    assert lista[0] == "hola"

def test_borra_lista():
    """ Prueba unitaria para borra_lista """
    lista = ["master", "full", "stack"]
    api.borra_lista(lista)
    assert not lista
