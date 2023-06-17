from states import states_airfyer

class PID: 
    def __init__(self):
        self.referencia = 0.0
        self.Kp = 30.0 # Ganho Proporcional
        self.Ki = 0.2  # Ganho Integral
        self.Kd = 400.0  # Ganho Derivativo
        self.T = 1.0      # Período de Amostragem (ms)
        self.erro_total = 0.0
        self.erro_anterior = 0.0
        self.sinal_de_controle_MAX = 100.0
        self.sinal_de_controle_MIN = -100.0

    def pid_configura_constantes(Kp_, Ki_, Kd_, self):
        self.Kp = Kp_
        self.Ki = Ki_
        self.Kd = Kd_


    def pid_controle(self):
        erro = states_airfyer["reference_temperature"] - states_airfyer["intern_temperature"]

        self.erro_total += erro

        if (self.erro_total >= self.sinal_de_controle_MAX):
            self.erro_total = self.sinal_de_controle_MAX
        elif (self.erro_total <= self.sinal_de_controle_MIN):
            self.erro_total = self.sinal_de_controle_MIN
        
        delta_error = erro - self.erro_anterior

        self.sinal_de_controle = self.Kp * erro + (self.Ki * self.T) * self.erro_total + (self.Kd / self.T) * delta_error

        if (self.sinal_de_controle >= self.sinal_de_controle_MAX):
            self.sinal_de_controle = self.sinal_de_controle_MAX
        elif (self.sinal_de_controle <= self.sinal_de_controle_MIN): 
            self.sinal_de_controle = self.sinal_de_controle_MIN
        
        self.erro_anterior = erro
        states_airfyer["control_signal"] = self.sinal_de_controle

        return self.sinal_de_controle
