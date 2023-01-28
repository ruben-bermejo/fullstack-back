""" Pruebas para el módulo calculadora """
import time
import calculadora

def test_sumar():
    """ Prueba para sumar """
    time.sleep(1)
    sumando_a = 2
    sumando_b = 2
    resultado = calculadora.sumar(sumando_a, sumando_b)
    assert resultado == 4

def test_restar():
    """ Prueba para restar """
    time.sleep(1)
    sustraendo_a = 2
    sustraendo_b = 2
    resultado = calculadora.restar(sustraendo_a, sustraendo_b)
    assert resultado == 0
