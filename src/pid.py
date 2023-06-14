from states import states_airfyer

referencia = 0.0
Kp = 30.0 # Ganho Proporcional
Ki = 0.2  # Ganho Integral
Kd = 400.0  # Ganho Derivativo
T = 1.0      # Período de Amostragem (ms)
erro_total = 0.0
erro_anterior = 0.0
sinal_de_controle_MAX = 100.0
sinal_de_controle_MIN = -100.0

def pid_configura_constantes(Kp_, Ki_, Kd_):
    Kp = Kp_
    Ki = Ki_
    Kd = Kd_


def pid_controle():
    global kp, ki, kd, erro_total, erro_anterior

    erro = states_airfyer["reference_temperature"] - states_airfyer["intern_temperature"]

    erro_total += erro # Acumula o erro (Termo Integral)

    if (erro_total >= sinal_de_controle_MAX): 
    
        erro_total = sinal_de_controle_MAX
    
    elif (erro_total <= sinal_de_controle_MIN): 
    
        erro_total = sinal_de_controle_MIN
    
    delta_error = erro - erro_anterior # Diferença entre os erros (Termo Derivativo)

    states_airfyer["control_signal"] = Kp*erro + (Ki*T)*erro_total + (Kd/T)*delta_error # PID calcula sinal de controle

    if (states_airfyer["control_signal"] >= sinal_de_controle_MAX):
        states_airfyer["control_signal"] = sinal_de_controle_MAX
    elif (states_airfyer["control_signal"] <= sinal_de_controle_MIN): 
        states_airfyer["control_signal"] = sinal_de_controle_MIN
    

    erro_anterior = erro

    return states_airfyer["control_signal"]
