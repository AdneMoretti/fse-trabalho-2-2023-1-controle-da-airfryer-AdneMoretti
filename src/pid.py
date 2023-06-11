#include "pid.h"
#include <stdio.h>

referencia = 0.0
Kp = 30.0 # Ganho Proporcional
Ki = 0.2  # Ganho Integral
Kd = 400.0  # Ganho Derivativo
T = 1.0      # Período de Amostragem (ms)
erro_total, erro_anterior = 0.0
sinal_de_controle_MAX = 100.0
sinal_de_controle_MIN = -100.0

def pid_configura_constantes(Kp_, Ki_, Kd_):
    Kp = Kp_
    Ki = Ki_
    Kd = Kd_


def pid_atualiza_referencia(referencia_):
    referencia = float(referencia_)


def pid_controle(saida_medida):

    erro = referencia - saida_medida

    erro_total += erro # Acumula o erro (Termo Integral)

    if (erro_total >= sinal_de_controle_MAX): 
    
        erro_total = sinal_de_controle_MAX
    
    elif (erro_total <= sinal_de_controle_MIN): 
    
        erro_total = sinal_de_controle_MIN
    

    delta_error = erro - erro_anterior # Diferença entre os erros (Termo Derivativo)

    sinal_de_controle = Kp*erro + (Ki*T)*erro_total + (Kd/T)*delta_error # PID calcula sinal de controle

    if (sinal_de_controle >= sinal_de_controle_MAX):
    
        sinal_de_controle = sinal_de_controle_MAX
    
    elif (sinal_de_controle <= sinal_de_controle_MIN): 
    
        sinal_de_controle = sinal_de_controle_MIN
    

    erro_anterior = erro

    return sinal_de_controle
